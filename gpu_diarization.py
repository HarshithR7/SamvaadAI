import torch
import torchaudio

from pyannote.audio import Pipeline
from datetime import timedelta

from pyannote.audio.pipelines.utils.hook import ProgressHook


pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization@2.1",
                                    use_auth_token="AUTH_KEY")
pipeline.to(torch.device("cuda"))

waveform, sample_rate = torchaudio.load("/mnt/c/Users/harsh/Downloads/18th_July_2025_Recording.wav")
diarization = pipeline({"waveform": waveform, "sample_rate": sample_rate})

with ProgressHook() as hook:
    diarization = pipeline({"waveform": waveform, "sample_rate": sample_rate}, hook=hook)

#diarization = pipeline("/content/sample_data", num_speakers=2)

# diarization = pipeline("audio.wav", min_speakers=2, max_speakers=5)
# dump the diarization output to disk using RTTM format
with open("diarization.txt", "w") as f:
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        start = str(timedelta(seconds=int(turn.start)))
        end = str(timedelta(seconds=int(turn.end)))
        f.write(f"{start} - {end}: {speaker}\n")
