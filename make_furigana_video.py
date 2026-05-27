from pathlib import Path
import argparse
import re
import subprocess

import pysubs2
from fugashi import Tagger


# ---------------- CONFIG ----------------

FONT_NAME = "Yu Gothic"
MAIN_FONT_SIZE = 48
FURIGANA_FONT_SIZE = 24

# Top-center subtitles
MAIN_MARGIN_V = 95
FURIGANA_MARGIN_V = 55

SHOW_FURIGANA = True

OUTPUT_ASS_NAME = "captions_furigana.ass"
OUTPUT_VIDEO_SUFFIX = "_furigana"
VIDEO_WIDTH = 1920
VIDEO_HEIGHT = 1080

SUBTITLE_Y = 135
FURIGANA_Y = 92

PX_PER_JA_CHAR = 54
TOKEN_GAP = 12

# ----------------------------------------


KANJI_RE = re.compile(r"[\u4E00-\u9FFF]")

def text_units(text: str) -> float:
    units = 0
    for ch in text:
        if ord(ch) < 128:
            units += 0.5
        else:
            units += 1
    return units


def tokenize_for_ruby(text: str, tagger: Tagger):
    tokens = []

    clean_text = " ".join(line.strip() for line in text.splitlines() if line.strip())

    for word in tagger(clean_text):
        surface = word.surface
        reading = get_reading(word)

        tokens.append({
            "surface": ass_escape(surface),
            "reading": ass_escape(reading) if has_kanji(surface) and reading else "",
            "units": text_units(surface),
        })

    return tokens

def has_kanji(text: str) -> bool:
    return bool(KANJI_RE.search(text))


def kata_to_hira(text: str) -> str:
    result = []
    for ch in text:
        code = ord(ch)
        if 0x30A1 <= code <= 0x30F6:
            result.append(chr(code - 0x60))
        else:
            result.append(ch)
    return "".join(result)


def ass_escape(text: str) -> str:
    return (
        text.replace("\\", "\\\\")
        .replace("{", "\\{")
        .replace("}", "\\}")
        .replace("\n", " ")
        .strip()
    )


def get_reading(word) -> str:
    feature = word.feature

    for attr in ("kana", "pron", "pronBase"):
        value = getattr(feature, attr, None)
        if value and value != "*":
            return kata_to_hira(value)

    return ""


def make_furigana_line(text: str, tagger: Tagger) -> str:
    parts = []

    for word in tagger(text):
        surface = word.surface
        reading = get_reading(word)

        if has_kanji(surface) and reading:
            parts.append(reading)
        else:
            # Rough spacing placeholder.
            # This is not perfect ruby alignment yet, but it keeps the MVP readable.
            parts.append("　" * max(1, len(surface)))

    return ass_escape(" ".join(parts)).strip()


def make_main_line(text: str) -> str:
    text = " ".join(line.strip() for line in text.splitlines() if line.strip())
    return ass_escape(text)


def build_ass_from_srt(srt_path: Path, ass_path: Path) -> None:
    tagger = Tagger()
    subs = pysubs2.load(str(srt_path), encoding="utf-8")

    out = pysubs2.SSAFile()
    out.info["PlayResX"] = str(VIDEO_WIDTH)
    out.info["PlayResY"] = str(VIDEO_HEIGHT)
    out.info["WrapStyle"] = "0"
    out.info["ScaledBorderAndShadow"] = "yes"

    black = pysubs2.Color(0, 0, 0, 0)
    white = pysubs2.Color(255, 255, 255, 0)

    out.styles["Main"] = pysubs2.SSAStyle(
        fontname=FONT_NAME,
        fontsize=MAIN_FONT_SIZE,
        primarycolor=black,
        outlinecolor=white,
        backcolor=white,
        shadow=0,
        outline=4,
        borderstyle=1,
        alignment=5,
    )

    out.styles["Furigana"] = pysubs2.SSAStyle(
        fontname=FONT_NAME,
        fontsize=FURIGANA_FONT_SIZE,
        primarycolor=black,
        outlinecolor=white,
        backcolor=white,
        shadow=0,
        outline=3,
        borderstyle=1,
        alignment=5,
    )

    for event in subs:
        tokens = tokenize_for_ruby(event.text, tagger)

        total_units = sum(t["units"] for t in tokens)
        total_width = total_units * PX_PER_JA_CHAR + max(0, len(tokens) - 1) * TOKEN_GAP

        x = (VIDEO_WIDTH - total_width) / 2

        for token in tokens:
            token_width = token["units"] * PX_PER_JA_CHAR
            token_center_x = x + token_width / 2

            main_text = r"{\pos(%d,%d)}%s" % (
                int(token_center_x),
                SUBTITLE_Y,
                token["surface"],
            )

            out.events.append(
                pysubs2.SSAEvent(
                    start=event.start,
                    end=event.end,
                    text=main_text,
                    style="Main",
                )
            )

            if SHOW_FURIGANA and token["reading"]:
                furigana_text = r"{\pos(%d,%d)}%s" % (
                    int(token_center_x),
                    FURIGANA_Y,
                    token["reading"],
                )

                out.events.append(
                    pysubs2.SSAEvent(
                        start=event.start,
                        end=event.end,
                        text=furigana_text,
                        style="Furigana",
                    )
                )

            x += token_width + TOKEN_GAP

    out.save(str(ass_path), encoding="utf-8")


def burn_subtitles(video_path: Path, ass_path: Path, output_path: Path) -> None:
    # Windows-friendly trick:
    # Run FFmpeg from the ASS file's folder so the ass filter only receives a simple filename.
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(video_path.resolve()),
        "-vf",
        f"ass={ass_path.name}",
        "-c:a",
        "copy",
        str(output_path.resolve()),
    ]

    subprocess.run(cmd, cwd=str(ass_path.parent.resolve()), check=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("video", help="Input MP4 file")
    parser.add_argument("srt", help="Input Japanese SRT file")
    parser.add_argument("--out", help="Output MP4 file", default=None)
    args = parser.parse_args()

    video_path = Path(args.video)
    srt_path = Path(args.srt)

    if not video_path.exists():
        raise FileNotFoundError(video_path)

    if not srt_path.exists():
        raise FileNotFoundError(srt_path)

    ass_path = srt_path.with_name(OUTPUT_ASS_NAME)

    if args.out:
        output_path = Path(args.out)
    else:
        output_path = video_path.with_name(
            video_path.stem + OUTPUT_VIDEO_SUFFIX + video_path.suffix
        )

    print("Creating ASS subtitles...")
    build_ass_from_srt(srt_path, ass_path)

    print("Burning subtitles into video...")
    burn_subtitles(video_path, ass_path, output_path)

    print(f"Done: {output_path}")


if __name__ == "__main__":
    main()
