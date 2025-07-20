from datetime import timedelta
from pyannote.audio import Pipeline

# Your Hugging Face token here
token = "AUTH_KEY"  

# Load diarization pipeline
diarization_pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization@2.1", use_auth_token=token)

# Run diarization
diarization = diarization_pipeline("/mnt/c/Users/harsh/Downloads/18th_July_2025_Recording.wav")


# Print speaker segments with hh:mm:ss format
for turn, _, speaker in diarization.itertracks(yield_label=True):
    start = str(timedelta(seconds=int(turn.start)))
    end = str(timedelta(seconds=int(turn.end)))
    print(f"{start} - {end}: {speaker}")