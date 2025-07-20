import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from datetime import timedelta

# Set device and model precision
device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

# Load Whisper large model
model_id = "openai/whisper-large-v3"
model = AutoModelForSpeechSeq2Seq.from_pretrained(
    model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
)
model.to(device)
processor = AutoProcessor.from_pretrained(model_id)

# Load pipeline
pipe = pipeline(
    "automatic-speech-recognition",
    model=model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    batch_size=4,
    torch_dtype=torch_dtype,
    device=device,
)

# Transcribe audio
result = pipe("/mnt/c/Users/harsh/Downloads/18th_July_2025_Recording.mp3", return_timestamps=True, generate_kwargs={"language": "english"})

# Process and convert timestamps to hh:mm:ss
chunks_in_clock = []
for chunk in result["chunks"]:
    start_sec, end_sec = chunk["timestamp"]

    # Guard against None values
    if start_sec is None or end_sec is None:
        continue

    # Convert to hh:mm:ss format
    start_time = str(timedelta(seconds=int(start_sec)))
    end_time = str(timedelta(seconds=int(end_sec)))
    
    chunks_in_clock.append({
        "start_time": start_time,
        "end_time": end_time,
        "text": chunk["text"]
    })

# Save transcript to a .txt file
output_file_path = "transcript_output.txt"
with open(output_file_path, "w", encoding="utf-8") as f:
    for c in chunks_in_clock:
        f.write(f"{c['start_time']} - {c['end_time']}: {c['text']}\n")

print(f"Transcript saved to {output_file_path}")
