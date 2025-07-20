````markdown
# 🪷 SamvaadAI (संवादAI) – Dialogue to Insight

**Samvaad** is an end-to-end meeting intelligence pipeline that converts raw meeting recordings into actionable insights using diarization, transcription, and OpenAI-powered summarization.

> संवाद (Samvaad) means *dialogue* or *conversation* in Sanskrit – symbolizing the core of this project: transforming conversations into structured knowledge.

---

## 📦 Project Overview

This project enables you to:

- 🎧 Convert recorded meetings into **audio** (mp3/wav)
- ✍️ Transcribe audio to **text**
- 🧑‍🤝‍🧑 Detect **who said what** with speaker diarization
- 📜 Structure transcripts by **speaker and timestamp**
- 🧠 Generate **meeting summaries**, **key points discussed**, and **action items** using OpenAI GPT

---

## 🛠️ Components & Workflow

### 1. 🎥 Convert Video to Audio
```bash
ffmpeg -i video.mp4 -q:a 0 -map a output.mp3
ffmpeg -i output.mp3 output.wav
````

---

### 2. 📝 Transcription

**Script:** `Audio_Transcribe`

* **Input:** `output.mp3`
* **Output:** `transcript_output.txt`

Generates raw transcription from the audio using Whisper or another speech-to-text model.

---

### 3. 👥 Speaker Diarization

**Script:** `gpu_diarization`

* **Input:** `output.wav`
* **Output:** `diarization.txt`

Identifies speakers and timestamps to allow tracking “who said what.”

---

### 4. 📚 Structuring the Transcript

**Script:** `structured_transcribe_diarization`

* **Input:** `transcript_output.txt`, `diarization.txt`
* **Output:** `final_speaker_transcript.txt`

Combines transcription and diarization into a structured, timestamped format ready for NLP processing.

---

### 5. 🧠 Meeting Summarization & Insights

**Script:** `summarization_openai.py`

* **Input:** `final_speaker_transcript.txt`
* **Output:** `meeting_summary_openai_structured.txt`
* **Requirement:** OpenAI API key (calls from `harshith.surakanti@gmail.com`)

Generates:

* 📌 A 5–7 sentence **meeting summary**
* 📍 **Key points** discussed with timestamps
* ✅ **Action items** per speaker with timestamps

---

## 💡 Example Output

```
📌 MEETING SUMMARY:
The meeting focused on planning the upcoming fundraiser, including ticketing, music, and social media promotion...

📍 KEY POINTS DISCUSSED:
Sandra shared event updates: 50 items for silent auction, raffle planning, online ticket sales via Bethany... (0:00)
Craig offered tech/design support... (0:00:32)

✅ ACTION ITEMS:
Sandra:
• Share social media copy with Craig’s team. (0:01:00)
Craig:
• Coordinate music with Matthew. (0:00:29)
```

---

## 🔐 API Key Setup

To use OpenAI summarization, set your API key inside `summarization_openai.py`:

```python
from openai import OpenAI
client = OpenAI(api_key="your-api-key-here")
```

---

## 📁 File Structure

```
Samvaad/
│
├── Audio_Transcribe.py
├── gpu_diarization.py
├── structured_transcribe_diarization.py
├── summarization_openai.py
│
├── transcript_output.txt
├── diarization.txt
├── final_speaker_transcript.txt
├── meeting_summary_openai_structured.txt
```

---

## 🤝 Contributors

* Harshith Surakanti

---

## 🙏 Acknowledgments

* OpenAI GPT for powerful summarization
* PyAnnote/Whisper for transcription and diarization
* ffmpeg for media processing

```

---

Let me know if you want a minimal or more technical version, or want to include badges, usage gifs, or requirements!
```
