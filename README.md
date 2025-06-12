# ML Annotation & Classification Toolkit
This repository contains annotation tools and ML classifiers for multiple data types. 
Tools support images, text, audio, and video with both annotation-only and full annotation + classification workflows.

## Annotation + Classification Tools
- **Image Annotation and Classification Tool**: Image annotation with PyTorch classifier; Annotates and classifies images (e.g., cats/dogs) using a Tkinter-based GUI.
- **Sarcasm Annotation and Classification Tool**: Text annotation with scikit-learn classifier; Annotates and classifies text for sarcasm using a Tkinter-based GUI.
- **Emotion and Intent Annotation and Classification Tool**: Text, audio, and video annotation with Hugging Face Transformers-based classifier; Annotates and classifies emotions and intents in text, audio, and video segments using a Tkinter-based GUI with AI suggestions and SHAP explainability.

## Annotation-Only Tools
- **Hypothesis Annotation Tool**: Text and image annotation; Annotates text hypotheses with or without corresponding images using a Tkinter-based GUI.
- **Bounding Box Annotation Tool**: Image annotation; Annotates objects in images with bounding boxes and text labels with a Tkinter-based GUI.

## Structure
### Annotation + Classification Tools
- `image_annotator/`: Annotates and classifies images
- `sarcasm_annotator/`: Annotates and classifies text for sarcasm
- `emotion_intent_annotator/`: Annotates and classifies emotions and intents in text, audio, and video

### Annotation-Only Tools
- `bounding_box_annotator/`: Annotates objects in images with bounding boxes and text labels
- `hypothesis_annotator/`: Annotates text hypotheses with or without corresponding images

## Installation
Each tool has its own requirements. See individual subfolder READMEs for setup instructions.
