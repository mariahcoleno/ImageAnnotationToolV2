# ML Annotation & Classification Toolkit
This repository contains annotation tools and ML classifiers for multiple data types. 
Tools support images, text, audio, and video with both annotation-only and full annotation + classification workflows.

## Annotation + Classification Tools
- **Image Annotation and Classification Tool**: Image annotation with PyTorch classifier; Annotates images (e.g., cats/dogs) with a Tkinter-based GUI.
- **Sarcasm Annotation and Classification Tool**: Text annotation with scikit-learn classifier; Annotates text as Sarcastic, Not Sarcastic, or Unsure with a Tkinter-based GUI.
- **Emotion and Intent Annotation and Classification Tool**: Text, audio, and video annotation with Hugging Face Transformers-based classifier; Annotates text, audio, and video segments with emotions (happy, sad, sarcastic, etc.) and intents (inform, persuade, etc.) using a Tkinter-based GUI and AI suggestions with SHAP explainability.

## Annotation-Only Tools
- **Hypothesis Annotation Tool**: Text and image annotation; Annotates hypotheses on images or text as Supported, Refuted, or Unsure with a Tkinter-based GUI.
- **Bounding Box Annotation Tool**: Image annotation; Annotates images with bounding boxes with a Tkinter-based GUI.

## Structure
### Annotation + Classification Tools
- `image_annotation/`: Image annotation and classification tool
- `sarcasm_annotation/`: Sarcasm annotation and classification tool
- `EmotionIntentAnnotator/`: Emotion and intent annotation and classification tool

### Annotation-Only Tools
- `bounding_box_annotation/`: Bounding box annotation tool
- `hypothesis_annotator/`: Hypothesis annotation tool

## Installation
Each tool has its own requirements. See individual subfolder READMEs for setup instructions.
