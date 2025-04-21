import whisper
import os
import torch
import warnings
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def process_audio(file_path):
    """
    Process audio or video file to extract transcriptions using Whisper.
    Returns list of text segments.
    """
    logger.debug(f"Processing file: {file_path}")
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        return []
    
    try:
        # Suppress FP16 warning and load model
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            logger.debug("Loading Whisper base model on CPU")
            model = whisper.load_model("base", device="cpu")
        
        # Transcribe with verbose output and language detection
        logger.debug("Starting transcription")
        result = model.transcribe(file_path, fp16=False, verbose=True, language="en")
        
        # Log raw result
        logger.debug(f"Transcription result: {result}")
        
        # Extract segments
        segments = result.get("segments", [])
        if not segments:
            logger.warning("No segments found in transcription")
            return []
        
        # Combine text if segments are too short, then re-segment in process_text
        text_segments = [seg["text"].strip() for seg in segments if seg["text"] and seg["text"].strip()]
        logger.debug(f"Extracted segments: {text_segments}")
        
        if not text_segments:
            logger.warning("No valid text segments after filtering")
            return []
        
        return text_segments
    except Exception as e:
        logger.error(f"Audio processing failed: {str(e)}")
        return []
