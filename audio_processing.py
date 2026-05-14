from config import whisper_model, diarization_pipeline

def transcribe_audio(path):

    segments, info = whisper_model.transcribe(path)

    transcript_data = []
    
    for segment in segments:
        transcript_data.append({
            "start" : segment.start,
            "end" : segment.end,
            "text": segment.text.strip()
        })
    
    return transcript_data


def diarize_audio(path):

    diarization = diarization_pipeline(path, num_speakers = 2)

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


