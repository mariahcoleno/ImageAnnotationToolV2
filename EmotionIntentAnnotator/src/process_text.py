import nltk
from transformers import pipeline

try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab')

try:
    emotion_classifier = pipeline(
        "text-classification",
        model="j-hartmann/emotion-english-distilroberta-base",
        top_k=None
    )
except Exception as e:
    print(f"Failed to load classifier: {e}")
    emotion_classifier = None

def segment_text(text):
    """Split text into sentences."""
    return nltk.sent_tokenize(text)

def suggest_text_emotion(segment):
    """Suggest emotion for a text segment."""
    if not emotion_classifier:
        print("Error: Emotion classifier not loaded")
        return "neutral"
    try:
        # Preprocess: If "just kidding" is present, focus on the main clause
        segment_lower = segment.lower()
        if "just kidding" in segment_lower:
            main_clause = segment_lower.split("just kidding")[-1].strip(", .")
            if main_clause:
                segment = main_clause
        results = emotion_classifier(segment)[0]
        print(f"Segment: {segment}, Model output: {results}")  # Debug
        top_emotion = max(results, key=lambda x: x["score"])["label"]
        return top_emotion
    except Exception as e:
        print(f"Error suggesting emotion: {e}")
        return "neutral"
