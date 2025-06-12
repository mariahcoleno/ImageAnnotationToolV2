### Emotion and Intent Annotation and Classification Tool 
This tool annotates and classifies text, audio, and video segments with emotions and intents using a Tkinter-based GUI with AI suggestions and SHAP explainability.

Thisels with explainability, editing segments, saving annotations, undoing, and exporting to CSV, designed for research and data preparation in NLP and multi-modal AI.

 Text, audio, and video annotation with Hugging Face Transformers-based classifier; Annotates and classifies emotions and intents in text, 
emotion_intent_annotator/: Annotates and classifies emotions and intents in text, audio, and video

### Overview
- Supports uploading text/audio/video files using a Tkinter-based GUI.
- Supports transcribing audio from media.
- Supports suggesting labels with explainability.
- Supports editing segments.
- Supports labeling text, audio, and video segments with emotions and intents and saving annotations.
- Supports undoing annotations and exporting to CSV.
- Built with Python, Tkinter, and SQLite.

### GUI Features
- Upload text files (.txt) or media files (.wav, .mp3, .m4a, .mp4, .mov).
- Transcribe audio from audio/video files to text using Whisper with consistent segmentation and punctuation cleanup.
- Segment text/transcriptions automatically, splitting before disclosure markers (e.g., "actually").
- Suggest emotions (happy, sad, sarcastic, angry, neutral) and intents (inform, persuade, joke, complain) with context-aware logic. 
- Visualize AI emotion suggestions using SHAP plots to show word contributions (e.g., "excited" boosts "happy").
- Edit text segments with save functionality.
- Save annotations to a SQLite database with filename support.
- Undo annotations.
- Export annotations to annotations_export.csv with media_id, filename, segment, emotion, intent, with success/warning popups.

### Feature Details
- Audio Annotation: Segment and annotate WAV files using librosa.
- Video Support: Extract frames and annotate using opencv.
- Explainability: Visualize AI suggestions with SHAP or matplotlib.

### Screenshots
#### GUI Screenshots
![GUI segment 1](screenshots/EmotionandIntentAnnotator_GUI_segment1.png)
![GUI segment 2](screenshots/EmotionandIntentAnnotator_GUI_segment2.png)

#### SHAP Visualizations
![SHAP Text Force Plot Segment 1](screenshots/shap_force_text_segment1.png)
![SHAP Text Force Plot Segment 2](screenshots/shap_force_text_segment2.png)
![SHAP Summary Plot Segment 1](screenshots/shap_summary_segment1.png)
![SHAP Summary Plot Segment 2](screenshots/shap_summary_segment2.png)
![SHAP Waterfall Plot Segment 1](screenshots/shap_waterfall_segment1.png)
![SHAP Waterfall Plot Segment 2](screenshots/shap_waterfall_segment2.png)

### Files
- `requirements.txt`: Lists all Python dependencies required to run the tool.
- `src/setup_db.py`: Initializes SQLite databse.
- `src/process_text.py`: Text segmentation and AI suggestions.
- `src/annotate_emotions.py`: The main script that runs a Tkinter-based GUI to display texts from `emotions_intents.sqlite` and save annotations (emotions/intents) to the database.
- `src/audio.py`: Handles audio transcriptions using openai-whisper and segments transcriptions for annotation. 
- `data/sample_text.txt`: File that contains sample texts.
- `data/sample_audio.m4a`: File that contains sample audio.
- `data/sample_audio.wav`: File that contains sample audio.
- `data/sample_video.mp4`: File that contains sample video.
- `emotions_intents.sqlite`: Generated SQLite database storing labeled texts (ignored by Git).
- `annotations_export.csv`: Exported CSV of labeled texts (ignored by Git).

### Requirements
- Python 3.8+ (required for some dependencies, tested with Python 3.13.3)

**Third-party packages:**
- pandas - for data manipulation and CSV handling
- torch - for PyTorch machine learning models
- transformers - for Hugging Face NLP models and pipelines (for emotion suggestions)
- textblob - for natural language processing
- shap - for model explainability
- matplotlib - for plotting and visualizations
- numpy - for numerical operations
- openai-whisper - for speech-to-text transcription
- nltk - for natural language toolkit (sentence segmentation)

**Python standard library modules used:**
- tkinter, sqlite3, os, sys, logging, traceback, warnings, re

### Setup and Usage
#### Option 1: From GitHub (Clone)
- **Note**:
  - Start in your preferred directory (e.g., cd ~/Desktop/ or cd ~/Downloads/ or cd ~/Documents/) to control where the repository clones. 
  - If you skip this step, it clones to your current directory.
1. Clone the repository: `git clone https://github.com/mariahcoleno/annotation-classification-toolkit.git`
2. Navigate to the emotion_intent_annotator directory: `cd emotion_intent_annotator/` (from the root of your cloned repository)
3. Create virtual environment: `python3 -m venv venv`
4. Activate: `source venv/bin/activate` # On Windows: venv\Scripts\activate
5. Install dependencies: `pip install -r requirements.txt`
6. Install ffmpeg (required for audio/video processing):
   - macOS: `brew install ffmpeg`
   - Ubuntu/Debian: `sudo apt-get install ffmpeg` 
   - Windows: Download from https://ffmpeg.org/download.html and add to PATH
7. Set environment variable to suppress tokenizers warning: `export TOKENIZERS_PARALLELISM=false`  
8. Proceed to the "Run the Tool" section below.

#### Option 2: Local Setup (Existing Repository)
1. Navigate to your local repository `cd ~/Documents/annotation-classification-toolkit/` # Adjust path as needed
2. Navigate to emotion_intent_annoator directory: `cd emotion_intent_annotator/`
3. Setup and activate a virtual environment:
   - If existing: `source venv/bin/activate` # Adjust path if venv is elsewhere
   - If new:
     - `python3 -m venv venv`
     - `source venv/bin/activate` # On Windows: venv\Scripts\activate
4. Install dependencies (if not already): `pip install -r requirements.txt` 
5. Install ffmpeg (required for audio/video processing):
   - macOS: `brew install ffmpeg`
   - Ubuntu/Debian: `sudo apt-get install ffmpeg`
   - Windows: Download from https://ffmpeg.org/download.html and add to PATH          
6. Set environment variable to suppress tokenizers warning: `export TOKENIZERS_PARALLELISM=false`
7. Proceed to the "Run the Tool" section below.

### Run the Tool (Both Options):
1. `python3 src/setup_db.py` to initialize the database.
2. `python3 -m src.annotate_emotions` to open a GUI to:
    1. Upload a text file (e.g., data/sample_text.txt) or media file (`.wav`, `.mp3`, `.m4a`, `.mp4`, `.mov`):
       - Click "Upload File", select a .txt file (e.g., data/sample_text.txt) or an audio or video file, and click "Open".
       - View segmented text/transcriptions (e.g., "I'm thrilled about this project! Just kidding, it's overwhelming." -> two segments); edit if needed using "Edit Text" and "Save Edit".
    2. Annotate:
       - View each segment in the GUI.
       - Click "Suggest Labels" to get AI-suggested emotions/intents.
       - Click "Visualize Suggestions" to see SHAP plots explaining AI emotion predictions.
       - Annotate each segment with emotions and intents.
       - Click "Save Annotation" to store in the database.
    3. Manage Annotations:
       - Use "Undo Last Annotation" to revert the last annotation.
       - Click "Export CSV" to save annotations as annotations_export.csv.    
3. **Optional**: To reset the database (e.g., to clear test data and start media_id at 1):
     - `mv emotions_intents.sqlite emotions_intents_backup_$(date +%F).sqlite`
     - `python3 src/setup_db.py`
    
### Sample Data
The repository includes an example text file for testing text segmentation and annotation:
- **`data/sample_text.txt`**: 
  ```text
  I’m thrilled about this project! Just kidding, it’s overwhelming.
  ```
  This file is used to demonstrate the GUI’s ability to segment text into sentences and annotate emotions and intents. You can also upload your own .txt files via the GUI.

### Project Structure
- data/
  - sample_audio.m4a # Example audio file
  - sample_audio.wav # Example audio file
  - sample_text.txt # Example text file
  - sample_video.mp4 # Example video file 
- src/
   - __init__.py
   - annotate_emotions.py # GUI for annotation
   - audio.py # Audio transcription and segmentation
   - process_text.py # Text segmentation and AI suggestions 

   - setup_db.py # Initializes SQLite database
- README.md
- requirements.txt

### Features
- Audio Annotation: Segment and annotate WAV files using librosa.
- Video Support: Extract frames and annotate using opencv.
- Explainability: Visualize AI suggestions with SHAP or matplotlib.

### Notes
- Ensure nltk.download('punkt_tab') is run for sentence segmentation (included in process_text.py).
- The database (emotions_intents.sqlite) is created automatically by setup_db.py.
- For issues, check Python 3.8+ and virtual environment activation.

