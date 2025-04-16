import whisper
from pydub import AudioSegment
import os
from src.process_text import segment_text
import string

def process_audio(file_path):
    """
    Transcribe audio file and segment the transcription.
    Supports .wav, .mp3, .m4a.
    Returns list of segments.
    """
    try:
        # Handle .m4a by converting to .wav
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".m4a":
            audio = AudioSegment.from_file(file_path, format="m4a")
            temp_path = file_path.replace(".m4a", "_temp.wav")
            audio.export(temp_path, format="wav")
            file_path = temp_path
        else:
            temp_path = None
        
        # Load Whisper model
        model = whisper.load_model("tiny")
        
        # Transcribe audio
        result = model.transcribe(file_path)
        transcription = result["text"].strip()
        
        # Remove trailing punctuation for consistency
        transcription = transcription.rstrip(string.punctuation)
        
        # Segment transcription
        segments = segment_text(transcription)
        
        # Clean up temp file
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
        
        return segments if segments else [transcription]
    except Exception as e:
        print(f"Audio processing failed: {e}")
        return []
