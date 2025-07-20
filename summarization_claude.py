import re
import requests
from pathlib import Path
from collections import defaultdict

# === Set your OpenRouter API key here ===
API_KEY = "OPENAI_API_KEY"  # Replace with your actual OpenRouter API key
MODEL = "anthropic/claude-3-opus"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    #"HTTP-Referer": "https://yourdomain.com",  # optional
    "X-Title": "TranscriptSummary"
}

# === Function to call Claude 3 via OpenRouter ===
def ask_claude(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

# === Speaker ID to Name mapping ===
speaker_name_map = {
    "SPEAKER_00": "Sandra Ulog",
    "SPEAKER_01": "Craig Kaufman",
    "SPEAKER_02": "Craig Kaufman"
}

# === Load transcript ===
with open("/mnt/c/Inference/final_speaker_transcript.txt", "r", encoding="utf-8") as f:
    transcript = f.read()

# === Parse speakers and timestamps ===
pattern = re.compile(r"(SPEAKER_\d+) – (\d+:\d+:\d+)\n(.+?)(?=\n\S|$)", re.DOTALL)
matches = pattern.findall(transcript)

speaker_segments = defaultdict(list)
all_segments = []

for speaker_id, time, text in matches:
    speaker_name = speaker_name_map.get(speaker_id, speaker_id)
    cleaned_text = text.strip().replace('\n', ' ')
    line = f"{time}: {cleaned_text}"
    speaker_segments[speaker_name].append(line)
    all_segments.append(line)

full_text = "\n".join(all_segments)

# === Step 1: Chunked Summary + Key Points
print("⏳ Generating chunked summaries with Claude 3 Opus...")

summary_outputs = []
chunks = [full_text[i:i+10000] for i in range(0, len(full_text), 10000)]

for i, chunk in enumerate(chunks):
    print(f"🔹 Summarizing chunk {i+1}/{len(chunks)}...")
    chunk_prompt = f"""
This is chunk {i+1} of a meeting transcript.

Tasks:
1. Write a concise 3–5 sentence summary for this chunk.
2. List key discussion points with any available timestamps.

Transcript:
{chunk}

Format:
📌 CHUNK SUMMARY {i+1}:
📍 KEY POINTS {i+1}:
"""
    result = ask_claude(chunk_prompt)
    summary_outputs.append(result.strip())

combined_summary = "\n\n".join(summary_outputs)

# === Step 2: Action Items per Speaker
print("⏳ Extracting action items by speaker...")

speaker_action_items = {}

for speaker, segments in speaker_segments.items():
    speaker_text = "\n".join(segments)
    prompt = f"""
You are reviewing a meeting transcript for the speaker {speaker}.

Extract only the **clear, timestamped action items** this speaker committed to or was responsible for.

Format:
• [timestamp] Action item

Transcript:
{speaker_text[:10000]}
"""
    result = ask_claude(prompt)
    speaker_action_items[speaker] = result.strip()

# === Save results to file ===
output_path = Path("meeting_summary_claude.txt")
with open(output_path, "w", encoding="utf-8") as f:
    f.write("📌 MEETING SUMMARY + KEY POINTS:\n")
    f.write(combined_summary + "\n\n")

    f.write("✅ ACTION ITEMS BY SPEAKER:\n")
    for speaker, items in speaker_action_items.items():
        f.write(f"\n{speaker}:\n")
        f.write(items + "\n")

print(f"\n🎉 Summary and action items saved to: {output_path.resolve()}")
