from pathlib import Path
import argparse
import re
import subprocess
import json

import pysubs2
from fugashi import Tagger


DEFAULT_CONFIG = {
    "font_name": "Yu Gothic",
    "main_font_size": 48,
    "furigana_font_size": 24,
    "show_furigana": True,
    "output_ass_name": "captions_furigana.ass",
    "output_video_suffix": "_furigana",
    "video_width": 1920,
    "video_height": 1080,
    "subtitle_y": 135,
    "furigana_y": 92,
    "px_per_ja_char": 50,
    "token_gap": 2
}

KANJI_RE = re.compile(r"[\u4E00-\u9FFF]")


def load_config(config_path: Path) -> dict:
    config = DEFAULT_CONFIG.copy()

    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as f:
            user_config = json.load(f)
        config.update(user_config)
    else:
        print(f"Config not found: {config_path}. Using defaults.")

    return config


def text_units(text: str) -> float:
    units = 0
    for ch in text:
        units += 0.5 if ord(ch) < 128 else 1
    return units


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


def build_ass_from_srt(srt_path: Path, ass_path: Path, config: dict) -> None:
    tagger = Tagger()
    subs = pysubs2.load(str(srt_path), encoding="utf-8")

    out = pysubs2.SSAFile()
    out.info["PlayResX"] = str(config["video_width"])
    out.info["PlayResY"] = str(config["video_height"])
    out.info["WrapStyle"] = "0"
    out.info["ScaledBorderAndShadow"] = "yes"

    black = pysubs2.Color(0, 0, 0, 0)
    white = pysubs2.Color(255, 255, 255, 0)

    out.styles["Main"] = pysubs2.SSAStyle(
        fontname=config["font_name"],
        fontsize=config["main_font_size"],
        primarycolor=black,
        outlinecolor=white,
        backcolor=pysubs2.Color(255, 255, 255, 80),
        shadow=0,
        outline=0,
        borderstyle=3,
        alignment=5,
    )

    out.styles["Furigana"] = pysubs2.SSAStyle(
        fontname=config["font_name"],
        fontsize=config["furigana_font_size"],
        primarycolor=black,
        outlinecolor=white,
        backcolor=pysubs2.Color(255, 255, 255, 80),
        shadow=0,
        outline=0,
        borderstyle=3,
        alignment=5,
    )
    out.styles["Box"] = pysubs2.SSAStyle(
        fontname="Arial",
        fontsize=1,
        primarycolor=pysubs2.Color(255, 255, 255, 0),
        outlinecolor=pysubs2.Color(255, 255, 255, 0),
        backcolor=pysubs2.Color(255, 255, 255, 0),
        shadow=0,
        outline=0,
        borderstyle=1,
        alignment=7,
    )

    for event in subs:
        tokens = tokenize_for_ruby(event.text, tagger)

        total_units = sum(t["units"] for t in tokens)
        total_width = (
            total_units * config["px_per_ja_char"]
            + max(0, len(tokens) - 1) * config["token_gap"]
        )

        box_padding_x = config.get("box_padding_x", 45)
        box_height = config.get("box_height", 120)
        box_y = config.get("box_y", 52)

        box_width = int(total_width + box_padding_x * 2)
        box_x = int((config["video_width"] - box_width) / 2)

        box_text = r"{\p1\alpha&H80&\pos(%d,%d)}m 0 0 l %d 0 l %d %d l 0 %d{\p0}" % (
            box_x,
            box_y,
            box_width,
            box_width,
            box_height,
            box_height,
        )

        out.events.append(
            pysubs2.SSAEvent(
                start=event.start,
                end=event.end,
                text=box_text,
                style="Box",
                layer=0,
            )
        )

        x = (config["video_width"] - total_width) / 2

        for token in tokens:
            token_width = token["units"] * config["px_per_ja_char"]
            token_center_x = x + token_width / 2

            main_text = r"{\pos(%d,%d)}%s" % (
                int(token_center_x),
                config["subtitle_y"],
                token["surface"],
            )

            out.events.append(
                pysubs2.SSAEvent(
                    start=event.start,
                    end=event.end,
                    text=main_text,
                    style="Main",
                    layer=1,
                )
            )

            if config["show_furigana"] and token["reading"]:
                furigana_text = r"{\pos(%d,%d)}%s" % (
                    int(token_center_x),
                    config["furigana_y"],
                    token["reading"],
                )

                out.events.append(
                    pysubs2.SSAEvent(
                        start=event.start,
                        end=event.end,
                        text=furigana_text,
                        style="Furigana",
                        layer=1,
                    )
                )

            x += token_width + config["token_gap"]

    out.save(str(ass_path), encoding="utf-8")


def burn_subtitles(video_path: Path, ass_path: Path, output_path: Path) -> None:
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
    parser.add_argument("video", help="Input MP4/MKV file")
    parser.add_argument("srt", help="Input Japanese SRT file")
    parser.add_argument("--out", help="Output video file", default=None)
    parser.add_argument("--config", help="Config JSON file", default="config.json")
    args = parser.parse_args()

    video_path = Path(args.video)
    srt_path = Path(args.srt)
    config = load_config(Path(args.config))

    if not video_path.exists():
        raise FileNotFoundError(video_path)

    if not srt_path.exists():
        raise FileNotFoundError(srt_path)

    ass_path = srt_path.with_name(config["output_ass_name"])

    if args.out:
        output_path = Path(args.out)
    else:
        output_path = video_path.with_name(
            video_path.stem + config["output_video_suffix"] + video_path.suffix
        )

    print("Creating ASS subtitles...")
    build_ass_from_srt(srt_path, ass_path, config)

    print("Burning subtitles into video...")
    burn_subtitles(video_path, ass_path, output_path)

    print(f"Done: {output_path}")


if __name__ == "__main__":
    main()
