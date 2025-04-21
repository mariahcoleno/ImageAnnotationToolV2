from transformers import pipeline
import re
import shap
import numpy as np

# Initialize emotion classifier and SHAP explainer
classifier = pipeline("text-classification", model="bhadresh-savani/distilbert-base-uncased-emotion", top_k=None)
explainer = shap.Explainer(classifier)

def segment_text(text):
    """
    Segment text based on discourse markers or punctuation.
    Returns list of segments.
    """
    discourse_markers = r'\b(but|however|actually|anyway|nevertheless)\b'
    segments = re.split(discourse_markers, text, flags=re.IGNORECASE)
    segments = [s.strip() for s in segments if s.strip()]
    cleaned_segments = []
    i = 0
    while i < len(segments):
        if i + 1 < len(segments) and re.match(discourse_markers, segments[i], re.IGNORECASE):
            combined = f"{segments[i]} {segments[i+1]}".strip()
            cleaned_segments.append(combined)
            i += 2
        else:
            cleaned_segments.append(segments[i])
            i += 1
    return cleaned_segments

def suggest_text_emotion(text):
    """
    Suggest emotion for a text segment using a transformer model.
    Returns emotion label and SHAP values for visualization.
    """
    try:
        # Get model predictions
        result = classifier(text)
        emotions = {item['label']: item['score'] for item in result[0]}
        predicted_emotion = max(emotions, key=emotions.get)
        
        # Compute SHAP values
        shap_values = explainer([text], fixed_context=1)
        
        return predicted_emotion, shap_values
    except Exception as e:
        print(f"Emotion suggestion failed: {e}")
        return "neutral", None
