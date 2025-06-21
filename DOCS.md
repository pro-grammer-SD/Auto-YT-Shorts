# Auto-YT-Shorts Generator Documentation

A Python tool to generate automated YouTube Shorts with AI-generated text, audio, images, and final video rendering.

---

## 📁 Project Structure

```
Auto-YT-Shorts/
├── main.py
├── modules/
│   ├── audio.py
│   ├── image.py
│   ├── text.py
│   └── video.py
├── utils/
│   └── roqe.py
├── fonts/
│   └── font.otf
├── media/
│   ├── audio/
│   ├── images/
│   └── video/
├── output/
└── .env
```

---

## ▶️ Usage

```bash
python main.py -make "TOPIC" [options]
```

### Required:

* `-make "TOPIC"` — the topic you want the video to be based on.

### Optional Flags:

* `-d`, `--delete` — deletes the `media/` folder before starting.
* `-ow`, `--overwrite` — allows overwriting the final output video if it already exists.
* `-fr`, `--forcerender` — forces video rendering if `audio/` and `images/` already exist, but skips regenerating them.
* `-h`, `--help` — shows usage/help.

---

## 🔁 Flow Summary

### 1. `make_text(topic)`

* Generates lines of content from the topic using AI (e.g. Gemini/GPT).

### 2. `make_audio(text, index)`

* Converts each line to audio using TTS and saves as `output_#.mp3`.

### 3. `make_image(text, index)`

* Generates an image for each line using AI image generation and saves as `image_#.png`.

### 4. `make_video(subtitle_text, overwrite)`

* Merges the audio/image pairs into a video.
* Adds subtitles.
* Outputs `final_video.mp4` inside `output/`.

---

## 🛠 `main.py` Logic

1. Parses CLI args.
2. If `-d` is passed, deletes existing `media/` folder.
3. Creates `media/` and switches into it.
4. Checks for existing `audio/` and `images/` with valid file pairs.
5. Based on `-ow` and `-fr`, decides whether to regenerate or reuse existing media.
6. If valid audio-image pairs are found, renders video.
7. Outputs `output/final_video.mp4`.

---

## 🚫 Error Handling

* **Quota Errors** (RESOURCE\_EXHAUSTED) are handled via `retry_on_quota_error` decorator from `utils/roqe.py`.
* Automatically extracts `retryDelay` from the error and sleeps before retrying.
* Displays all user-facing errors via `rich` console.

---

## 🧪 Testing

```bash
# Clean full build
python main.py -make "The future of AI" -d -ow

# Skip regen and reuse if exists
python main.py -make "The future of AI" -fr

# Only force overwrite video output
python main.py -make "The future of AI" -ow
```

---

## 🧩 Dependencies

* `rich`
* `Pillow`
* `moviepy`
* `google.generativeai`
* `.env` for API keys (Gemini, etc.)

---

## 🔐 .env File Format

```
GOOGLE_API_KEY=your-api-key-here
```

---

## ⚠️ Known Issues

* Audio/image files must be correctly named (`output_#.mp3`, `image_#.png`) to be matched.
* Without matching pairs, video won't render.
* Exceeding API quota returns a wait time that is automatically respected.

---

## 📌 Final Notes

* Use `-d -ow` to rebuild everything from scratch.
* Use `-fr` when you already have the audio and images and just want a new video.
* Use `-c or --cleanup` to clean output
and exit.
* Your final video appears at: `output/final_video.mp4`

---

**Author:** Soumalya Das
**Tool:** Auto YT Shorts Generator
**Mode:** Overengineered but worth it 🚀
