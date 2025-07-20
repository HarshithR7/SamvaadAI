import re
from pathlib import Path
from collections import defaultdict
import ollama

# === Speaker ID to Name mapping ===
speaker_name_map = {
    "SPEAKER_00": "Sandra Ulog",
    "SPEAKER_01": "Craig Kaufman",
    "SPEAKER_02": "Craig Kaufman"
}

# === Load transcript file ===
with open("/mnt/c/Inference/final_speaker_transcript.txt", "r", encoding="utf-8") as f:
    transcript = f.read()

# === Parse speakers and timestamps ===
pattern = re.compile(r"(SPEAKER_\d+) – (\d+:\d+:\d+)\n(.+?)(?=\n\S|$)", re.DOTALL)
matches = pattern.findall(transcript)

# === Organize segments ===
speaker_segments = defaultdict(list)
all_segments = []

for speaker_id, time, text in matches:
    speaker_name = speaker_name_map.get(speaker_id, speaker_id)
    cleaned_text = text.strip().replace('\n', ' ')
    line = f"{time}: {cleaned_text}"
    speaker_segments[speaker_name].append(line)
    all_segments.append(line)

# === Full transcript text for meeting summary ===
full_text = "\n".join(all_segments)

# === Function to call Ollama model ===
def ask_ollama(prompt):
    response = ollama.chat(model='mistral', messages=[
        {"role": "user", "content": prompt}
    ])
    return response['message']['content']

# === Step 1: Chunked Summary + Key Points
summary_outputs = []

for i, chunk in enumerate([full_text[i:i+10000] for i in range(0, len(full_text), 10000)]):
    print(f"⏳ Summarizing chunk {i+1} via Ollama...")
    chunk_prompt = f"""
This is part {i+1} of a meeting transcript.

Your task:
1. Provide a concise 3–5 sentence summary for this chunk.
2. List key points discussed using bullets (with timestamps).

Transcript:
{chunk}

Format:
📌 CHUNK SUMMARY:
📍 KEY POINTS:
"""
    result = ask_ollama(chunk_prompt)
    summary_outputs.append(result.strip())

ollama_output = "\n\n".join(summary_outputs)

# === Step 2: Action Items per Speaker ===
print("\n⏳ Extracting speaker-specific action items...")

speaker_action_items = {}

for speaker, segments in speaker_segments.items():
    speaker_text = "\n".join(segments)
    speaker_prompt = f"""
You are reviewing a meeting transcript for {speaker}.
Extract clear, timestamped action items this person mentioned or committed to.
Format:
• [timestamp] Action item

Transcript:
{speaker_text[:6000]}
"""
    result = ask_ollama(speaker_prompt)
    speaker_action_items[speaker] = result.strip()

# === Save everything to file ===
output_path = Path("meeting_summary_ollama.txt")
with open(output_path, "w", encoding="utf-8") as f:
    f.write("📌 MEETING SUMMARY + KEY POINTS:\n")
    f.write(ollama_output.strip() + "\n\n")

    f.write("✅ ACTION ITEMS BY SPEAKER:\n")
    for speaker, items in speaker_action_items.items():
        f.write(f"\n{speaker}:\n")
        f.write(items.strip() + "\n")

print(f"\n🎉 Summary and action items saved to: {output_path.resolve()}")
