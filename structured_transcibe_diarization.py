import re
from datetime import timedelta

def hms_to_seconds(hms):
    h, m, s = map(int, hms.split(":"))
    return h * 3600 + m * 60 + s

def seconds_to_hms(seconds):
    return str(timedelta(seconds=int(seconds)))

# Load diarization segments
def load_diarization(file_path):
    diarization = []
    with open(file_path, "r") as f:
        for line in f:
            match = re.match(r"(\d+):(\d+):(\d+) - (\d+):(\d+):(\d+): SPEAKER_(\d+)", line.strip())
            if match:
                h1, m1, s1, h2, m2, s2, speaker_id = match.groups()
                start = int(h1)*3600 + int(m1)*60 + int(s1)
                end = int(h2)*3600 + int(m2)*60 + int(s2)
                speaker = f"SPEAKER_{speaker_id}"
                diarization.append({"start": start, "end": end, "speaker": speaker})
    return diarization

# Load transcript lines
def load_transcript(file_path):
    transcript = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            match = re.match(r"(\d+:\d+:\d+) - (\d+:\d+:\d+): (.+)", line.strip())
            if match:
                start_hms, end_hms, text = match.groups()
                start_sec = hms_to_seconds(start_hms)
                end_sec = hms_to_seconds(end_hms)
                midpoint = (start_sec + end_sec) / 2
                transcript.append({
                    "timestamp": start_hms,
                    "midpoint": midpoint,
                    "text": text
                })
    return transcript

# Align speaker segments to transcript
def align(transcript, diarization):
    aligned = []
    for line in transcript:
        speaker = "UNKNOWN"
        for d in diarization:
            if d["start"] <= line["midpoint"] <= d["end"]:
                speaker = d["speaker"]
                break
        aligned.append({
            "speaker": speaker,
            "timestamp": line["timestamp"],
            "text": line["text"]
        })
    return aligned

# Save final transcript
def save_output(data, out_path):
    with open(out_path, "w", encoding="utf-8") as f:
        for entry in data:
            f.write(f"{entry['speaker']} – {entry['timestamp']}\n{entry['text']}\n\n")
    print(f"✅ Final speaker-attributed transcript saved to: {out_path}")

# === MAIN ===
if __name__ == "__main__":
    diarization = load_diarization("/mnt/c/Inference/diarization.txt")  # adjust if needed
    transcript = load_transcript("/mnt/c/Inference/transcript_output.txt")
    aligned = align(transcript, diarization)
    save_output(aligned, "final_speaker_transcript.txt")
