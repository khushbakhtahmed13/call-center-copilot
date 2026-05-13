from faster_whisper import WhisperModel
from pyannote.audio import Pipeline
from dotenv import load_dotenv
import os

load_dotenv()

model = WhisperModel("base", device = "cpu", compute_type = "int8")

def transcribe_audio(path):

    segments, info = model.transcribe(path)

    transcript_data = []
    
    for segment in segments:
        transcript_data.append({
            "start" : segment.start,
            "end" : segment.end,
            "text": segment.text.strip()
        })
    
    return transcript_data

HF_TOKEN = os.getenv("HF_TOKEN")
pipeline = Pipeline.from_pretrained(
            "pyannote/speaker-diarization-3.1",
            token = HF_TOKEN
    )

def diarize_audio(path):

    diarization = pipeline(path, num_speakers = 2)

    diarize_data = []

    for segment, track, speaker in diarization.speaker_diarization.itertracks(yield_label = True):
        diarize_data.append({
            "start" : segment.start,
            "end" : segment.end,
            "speaker": speaker
        })
    
    return diarize_data
    
def get_final_transcript(path):
    transcript_segments = transcribe_audio(path)
    diarize_segments = diarize_audio(path)

    final_transcript = []

    for t in transcript_segments:
        t_start = t.get("start")
        t_end = t.get("end")

        max_overlap = 0
        speaker = "unknown"

        for s in diarize_segments:
            s_start = s.get("start")
            s_end = s.get("end")

            overlap = min(t_end, s_end) - max(t_start, s_start)

            if overlap > max_overlap:
                max_overlap = overlap
                speaker = s.get("speaker")
        
        
        final_transcript.append({
                  "speaker" : speaker,
                  "start" : t_start,
                  "end" : t_end,
                  "text" : t.get("text")
        })
    
    return final_transcript




if __name__ == "__main__":
    path = "data/calls/synthetic_bank_call.wav"
    try:
       #transcript_data = transcribe_audio(path)
       #print(transcript_data)
       #diarize_data = diarize_audio(path)
       final_transcript = get_final_transcript(path)
       for entry in final_transcript:
           print(entry)
    except Exception as e:
        print(f"Error: {e}")