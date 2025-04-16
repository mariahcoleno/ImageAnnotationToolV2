import nltk
from transformers import pipeline

nltk.download('punkt', quiet=True)

def segment_text(text):
    """
    Segment text into meaningful units, handling missing punctuation.
    Returns list of segments.
    """
    if not text:
        return []
    
    # Try NLTK sentence tokenizer first
    segments = nltk.sent_tokenize(text)
    
    # If only one segment (e.g., no punctuation), split before discourse markers
    if len(segments) <= 1:
        markers = ['actually', 'but', 'however', 'so', 'well', 'anyway']
        segments = []
        current = ""
        words = text.split()
        for i, word in enumerate(words):
            if word.lower() in markers and current.strip():
                segments.append(current.strip())
                current = word + " "
            else:
                current += word + " "
        if current.strip():
            segments.append(current.strip())
    
    # Clean up segments
    segments = [s.strip() for s in segments if s.strip()]
    return segments if segments else [text]

def suggest_text_emotion(text):
    """
    Suggest emotion for a text segment using a pre-trained model.
    Returns predicted emotion.
    """
    try:
        classifier = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")
        result = classifier(text)[0]
        return result['label'].lower()
    except Exception as e:
        print(f"Emotion suggestion failed: {e}")
        return "neutral"
