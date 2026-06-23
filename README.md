# Furigana Assist

日本語教育者・学習者・コンテンツ制作者向けのシンプルなツールです。

Furigana Assist は、日本語の SRT 字幕をふりがな付きの ASS 字幕へ変換し、FFmpeg を使って動画に字幕を焼き込むことができます。

日本語学習動画向けの見やすいふりがな字幕を、できるだけ少ない手間で作成できるようにすることを目的としています。

## このプロジェクトについて

私は日本語を勉強している学習者であり、ソフトウェア開発が好きな個人開発者です。

日本語学習コンテンツを見ている中で、ふりがな付き字幕の作成にはかなりの手作業が必要そうだと感じました。そこで、まずはその作業の一部を自動化できるシンプルなツールを作ってみようと思いました。

このプロジェクトは、動画編集ソフトや字幕編集ソフト、文字起こしツールの代わりになることを目指しているわけではありません。

対象としているのは、次のようなシンプルなワークフローです。

**完成した動画 + 完成した日本語字幕 → ふりがな付き字幕動画**

---

## 主な機能

* 日本語 SRT 字幕の読み込み
* Fugashi + UniDic を利用した自動ふりがな生成
* ASS 字幕ファイルの生成
* 漢字の上にふりがなを表示
* 字幕デザインのカスタマイズ
* FFmpeg による動画への字幕焼き込み
* サンプルファイル同梱

---

## 使い方

1. 動画を通常どおり編集する
2. 完成した動画を MP4 として書き出す
3. 修正済みの日本語字幕を SRT として用意する
4. Furigana Assist を実行する

出力されるもの：

* ASS 字幕ファイル
* ふりがな付き字幕を焼き込んだ動画

---

## 必要なもの

### リリースに含まれるもの

* Furigana Assist 実行ファイル
* サンプル動画
* サンプル字幕ファイル
* 設定ファイル

### 別途必要なもの

* FFmpeg

FFmpeg をインストールし、システムの PATH に追加してください。

---

## 設定

字幕の見た目は設定ファイルから変更できます。

設定例：

* フォント
* 字幕サイズ
* ふりがなサイズ
* 字幕位置
* 字幕ボックスのデザイン
* 動画解像度

---

## 例

入力：

日本語を勉強しています。

生成例：

日(に)本(ほん)語(ご)を勉強(べんきょう)しています。

実際の動画では、漢字の上にふりがなが表示されます。

---

## 現在の制限事項

* ふりがなの精度は使用する辞書や解析結果に依存します
* 一部の単語で誤った読みが生成される場合があります
* 修正済みの字幕ファイルが必要です
* 自動文字起こし機能は含まれていません
* 初期リリースのため、不具合が含まれている可能性があります

---

## 今後の予定

将来的に追加を検討している機能：

* 読み方の上書き辞書
* シンプルな GUI
* 字幕プレビュー
* バッチ処理の改善
* 自動文字起こし対応
* スタイルプリセット
* 単語リスト出力
* Anki デッキ生成

---

## フィードバック募集中

このプロジェクトで一番知りたいことは、

**「そもそも、この問題は解決する価値があるのか？」**

という点です。

もし日本語学習コンテンツを制作している方がいましたら、ぜひ以下について教えてください。

* 現在の字幕作成ワークフロー
* ふりがなをどのように付けているか
* 特に時間がかかる部分
* 既に利用している便利なツール

「すでにもっと良いツールがある」という意見も大歓迎です。

連絡先：

[seanakut@gmail.com](mailto:seanakut@gmail.com)

---

## ライセンス

MIT License

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
