
````markdown
# 🔧 What is `ffmpeg`?

`ffmpeg` is a free, open-source command-line tool used to process multimedia files. It can:

- 🎛️ Convert
- 🎥 Record
- 📡 Stream
- 🎙️ Extract
- ✂️ Edit
- 📦 Compress
- 🔍 Analyze

`ffmpeg` works with nearly any audio, video, or image format.

---

## ✅ Common Use Cases for `ffmpeg`

### 🎧 Audio

- **Convert formats** (`mp3`, `wav`, `aac`, `ogg`, etc.)
```bash
  ffmpeg -i input.wav output.mp3
```

* **Extract audio from video**

 ```bash
  ffmpeg -i video.mp4 -q:a 0 -map a output.mp3
  ```

* **Change sample rate or audio channels**

```bash
  ffmpeg -i input.wav -ar 16000 -ac 1 output.wav
```

---

### 🎥 Video

* **Convert formats** (`mp4`, `avi`, `mkv`, `mov`, etc.)

  ```bash
  ffmpeg -i input.avi output.mp4
  ```

* **Compress a video**

  ```bash
  ffmpeg -i input.mp4 -vcodec libx265 -crf 28 output.mp4
  ```

* **Cut/trim a video**

  ```bash
  ffmpeg -ss 00:00:10 -t 00:00:20 -i input.mp4 -c copy trimmed.mp4
  ```

* **Merge audio and video**

  ```bash
  ffmpeg -i video.mp4 -i audio.mp3 -c:v copy -c:a aac output.mp4
  ```

---

### 📸 Images

* **Extract frames from video**

  ```bash
  ffmpeg -i video.mp4 -r 1 image_%03d.png
  ```

* **Convert images to video**

  ```bash
  ffmpeg -framerate 1 -i image_%03d.png -c:v libx264 -r 30 output.mp4
  ```

---

### 📺 Streaming

* **Stream to RTMP server**

  ```bash
  ffmpeg -re -i input.mp4 -f flv rtmp://yourserver/live/stream
  ```

* **Record screen and audio**

  ```bash
  ffmpeg -f x11grab -s 1920x1080 -i :0.0 -f alsa -i default output.mkv
  ```

---

### 🧪 Filters and Effects

* **Add watermark/logo**

  ```bash
  ffmpeg -i input.mp4 -i logo.png -filter_complex "overlay=10:10" output.mp4
  ```

* **Add subtitles**

  ```bash
  ffmpeg -i input.mp4 -vf subtitles=subs.srt output.mp4
  ```

* **Speed up video**

  ```bash
  ffmpeg -i input.mp4 -filter:v "setpts=0.5*PTS" output.mp4
  ```

---

### 🧰 Other Utilities

* **Probe metadata**

  ```bash
  ffmpeg -i input.mp4
  ```

* **Burn in subtitles**

  ```bash
  ffmpeg -i input.mp4 -vf "subtitles=subs.srt" output.mp4
  ```

* **Normalize audio levels**

  ```bash
  ffmpeg -i input.mp3 -af "loudnorm" output.mp3
  ```

---

## 🧠 How Many Ways Can You Use `ffmpeg`?

Realistically, **hundreds**, if not **thousands**, depending on:

* Format combinations
* Filters and effects
* Stream configurations
* Encoding options
* Platforms (desktop, mobile, web)

---

> 🎯 **Need something specific?**
> Tell me your use case (e.g., podcasting, surveillance, machine learning), and I’ll tailor the list to your needs!

```

---

Just copy that into a `.md` file (e.g., `ffmpeg-guide.md`) on GitHub and it will render beautifully. Let me know if you want this as a downloadable file.
```
