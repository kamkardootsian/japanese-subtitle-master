# Furigana Assist

A simple tool for Japanese educators, learners, and content creators.

Furigana Assist converts Japanese SRT subtitles into styled ASS subtitles with furigana and can burn those subtitles directly into a video using FFmpeg.

The goal is to make it easier to create Japanese-learning videos with readable furigana subtitles while reducing repetitive formatting work.

---

## Why This Exists

I'm a Japanese learner and software enthusiast.

While watching Japanese learning content, I noticed that creating furigana subtitles appears to require a lot of manual work. Before spending time building something more complex, I wanted to create a simple tool that could automate part of that process.

This project is not intended to replace video editors, subtitle editors, or transcription tools. Instead, it focuses on a specific workflow:

> Finished video + finished Japanese subtitles → video with furigana subtitles

---

## Features

* Import Japanese SRT subtitles
* Automatic furigana generation using Fugashi + UniDic
* Generate styled ASS subtitles
* Furigana displayed above kanji
* Configurable subtitle appearance
* Burn subtitles directly into video using FFmpeg
* Sample files included

---

## Workflow

1. Edit your video normally
2. Export your final video as MP4
3. Export or create your corrected Japanese subtitles as SRT
4. Run Furigana Assist
5. Receive:

   * ASS subtitle file
   * Video with furigana subtitles burned in

---

## Requirements

### Included in Release

* Furigana Assist executable
* Sample video
* Sample subtitle file
* Example configuration

### Required

* FFmpeg

Download FFmpeg and make sure it is available in your system PATH.

---

## Configuration

Most appearance settings can be adjusted in the configuration file.

Examples include:

* Font name
* Main subtitle size
* Furigana size
* Subtitle position
* Subtitle box styling
* Video dimensions

---

## Example

Input:

```text
日本語を勉強しています。
```

Output:

```text
日(に)本(ほん)語(ご)を勉強(べんきょう)しています。
```

Rendered as Japanese text with furigana displayed above the kanji.

---

## Current Limitations

* Furigana accuracy depends on tokenizer readings
* Some words may receive incorrect readings
* Creator-provided subtitles are required
* Automatic transcription is not included
* Early release; bugs may exist

---

## Roadmap

Potential future features:

* Reading override dictionary
* Simple GUI
* Subtitle preview window
* Batch processing improvements
* Automatic transcription support
* Style presets
* Vocabulary export
* Anki deck generation

---

## Feedback Wanted

The biggest question behind this project is:

**Is this actually a problem worth solving?**

If you create Japanese-learning content, I'd love feedback on:

* Your subtitle workflow
* How you currently handle furigana
* What parts take the most time
* Existing tools I should know about

Even "this already exists" is valuable feedback.

Email: seanakut@gmail.com

---

## License

MIT License
