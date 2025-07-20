

import re
import time
from pathlib import Path
from collections import defaultdict
from openai import OpenAI

# === Set up OpenAI client ===
client = OpenAI(api_key="OPENAI_API_KEY")  # Replace with your actual OpenAI API key

# === Helper: Retry wrapper ===
def safe_call(call_fn, retries=3, wait=5):
    for attempt in range(retries):
        try:
            return call_fn()
        except Exception as e:
            print(f"⚠️ Error: {e}. Retrying in {wait} seconds...")
            time.sleep(wait)
    raise RuntimeError("Max retries exceeded.")

# === Helper: Chunk long text ===
def chunk_text(text, chunk_size=12000):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

# === Load and parse transcript ===
transcript_file = "/mnt/c/Inference/final_speaker_transcript.txt"
with open(transcript_file, "r", encoding="utf-8") as f:
    content = f.read()

pattern = re.compile(r"(SPEAKER_\d+) – (\d+:\d+:\d+)\n(.+?)(?=\n\S|$)", re.DOTALL)
matches = pattern.findall(content)

# === Speaker mapping ===
speaker_name_map = {
    "SPEAKER_00": "Sandra Ugol",
    "SPEAKER_01": "Craig Kaufman",
    "SPEAKER_02": "Craig Kaufman"
}

# === Organize segments ===
speaker_segments = defaultdict(list)
chronological_segments = []

for speaker_id, timestamp, text in matches:
    speaker = speaker_name_map.get(speaker_id, speaker_id)
    cleaned_text = text.strip().replace("\n", " ")
    speaker_segments[speaker].append(f"{timestamp}: {cleaned_text}")
    chronological_segments.append((timestamp, speaker, cleaned_text))

combined_text = "\n".join([f"{speaker} ({timestamp}): {text}" for timestamp, speaker, text in chronological_segments])
chunks = chunk_text(combined_text)

# === Step 1: Generate summary in chunks ===
print("⏳ Generating meeting summary...")
summary_parts = []
for chunk in chunks:
    response = safe_call(lambda: client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant summarizing transcripts."},
            {"role": "user", "content": f"Transcript:\n{chunk}\n\nWrite a concise 3–5 sentence summary of this section."}
        ],
        temperature=0.3
    ))
    summary_parts.append(response.choices[0].message.content.strip())

summary_output = "\n".join(summary_parts)

# === Step 2: Key Points (chronological) ===
print("⏳ Extracting key points in order...")
chronological_text = "\n".join([f"{timestamp}: {speaker}: {text}" for timestamp, speaker, text in chronological_segments])
point_chunks = chunk_text(chronological_text)

key_points = []
for chunk in point_chunks:
    response = safe_call(lambda: client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are an assistant extracting key points from a meeting transcript."},
            {"role": "user", "content": f"""
From the transcript below, extract key points **in sequence** of time. Include speaker name, main message, and timestamp.

Format:
Speaker shared this key point. (timestamp)

Transcript:
{chunk}
"""}
        ],
        temperature=0.3
    ))
    key_points.append(response.choices[0].message.content.strip())

key_points_output = "\n".join(key_points)

# === Step 3: Action items by speaker ===
print("⏳ Extracting action items by speaker...")
action_items_by_speaker = {}

for speaker, segments in speaker_segments.items():
    speaker_text = "\n".join(segments)
    speaker_chunks = chunk_text(speaker_text, 8000)

    speaker_items = []
    for chunk in speaker_chunks:
        response = safe_call(lambda: client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant extracting action items from a transcript."},
                {"role": "user", "content": f"""
Extract clear, timestamped action items from this transcript spoken by {speaker}.
Format:
Action description. (timestamp)

Transcript:
{chunk}
"""}
            ],
            temperature=0.3
        ))
        speaker_items.append(response.choices[0].message.content.strip())

    action_items_by_speaker[speaker] = "\n".join(speaker_items)

# === Save output to file ===
output_path = Path("meeting_summary_openai_structured.txt")
with open(output_path, "w", encoding="utf-8") as f:
    f.write("📌 MEETING SUMMARY:\n\n")
    f.write(summary_output + "\n\n")
    f.write("="*80 + "\n\n")

    f.write("📍 KEY POINTS DISCUSSED:\n\n")
    f.write(key_points_output + "\n\n")
    f.write("="*80 + "\n\n")

    f.write("✅ ACTION ITEMS:\n\n")
    for speaker, actions in action_items_by_speaker.items():
        f.write(f"{speaker}:\n{actions}\n\n")

print(f"✅ All outputs saved to: {output_path.resolve()}")
