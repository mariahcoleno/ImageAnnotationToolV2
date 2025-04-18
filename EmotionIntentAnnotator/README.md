# ImageAnnotationToolV2
### Emotion and Intent Annotator 
A GUI-based tool for annotating text, audio, and video segments with emotions and intents, built with Python, tkinter, and SQLite. This tool supports uploading text/audio/video files, transcribing audio from media, suggesting labels, editing segments, saving annotations, undoing, and exporting to CSV, designed for research and data preparation in NLP and multi-modal AI.

### Overview
- Labels text emotion and intent with a user-friendly GUI.
- Supports undoing annotations and exporting to CSV.
- Stores texts and annotations in SQLite with robust constraints.

### GUI Features
- Upload text files (.txt) or media files (.wav, .mp3, .m4a, .mp4, .mov).
- Transcribe audio from audio/video files to text using Whisper with consistent segmentation and punctuation cleanup.
- Segment text/transcriptions automatically, splitting before disclosure markers (e.g., "actually").
- Suggest emotions (happy, sad, sarcastic, angry, neutral) and intents (inform, persuade, joke, complain) with context-aware logic. 
- Edit text segments with save functionality.
- Save annotations to a SQLite database with filename support.
- Undo annotations.
- Export annotations to annotations_export.csv with media_id, segment, emotion, intent, with success/warning popups.

### Feature Details
- Audio Annotation: Segment and annotate WAV files using librosa.
- Video Support: Extract frames and annotate using opencv.
- Explainability: Visualize AI suggestions with SHAP or matplotlib.

### Screenshots
![EmotionIntentAnnotator GUI example 1](screenshots/emotionintentannotator_gui_text_audio_video_1.png)
![EmotionIntentAnnotator GUI example 2](screenshots/emotionintentannotator_gui_text_audio_video_2.png)

### Files
- `requirements.txt`: Lists dependencies required to run scripts.
- `src/setup_db.py`: Initializes SQLite databse.
- `src/process_text.py`: Text segmentation and AI suggestions.
- `src/annotate_emotions.py`: The main script that runs a Tkinter-based GUI to display texts from `emotions_intents.sqlite` and save annotations (emotions/intents) to the database.
- `src/audio.py`: Handles audio transcriptions using openai-whisper and segments transcriptions for annotation. 
- `data/sample_text.txt`: File that contains sample texts.
- `emotions_intents.sqlite`: Generated SQLite database storing labeled texts (ignored by Git).
- `annotations_export.csv`: Exported CSV of labeled texts (ignored by Git).

### Setup and Usage
#### Option 1: From GitHub (Clone)
- **Note**:
  - Start in your preferred directory (e.g., cd ~/Desktop/ or cd ~/Downloads/ or cd ~/Documents/) to control where the repository clones. 
  - If you skip this step, it clones to your current directory.
1. Clone the repository: `git clone https://github.com/mariahcoleno/ImageAnnotationToolV2.git`
2. Navigate to the sarcasm_annotation directory: `cd EmotionIntentAnnotator/` (from the root of your cloned repository)
3. Create virtual environment: `python3 -m venv venv`
4. Activate: `source venv/bin/activate` # On Windows: venv\Scripts\activate
5. Install dependencies: `pip install -r requirements.txt`
6. Install ffmeg (required for audio/video processing): `brew install ffmpeg` # macOS
                                                        `sudo apt-get install ffmpeg` # Ubuntu/Debian
                                                        Download from https://ffmpeg.org/download.html and add to PATH # Windows  
7. Proceed to the "Run the Tool" section below.

#### Option 2: Local Setup (Existing Repository)
1. Navigate to your local repository `cd ~/Documents/AnnotationProject/` # Adjust path as needed
2. Navigate to EmotionIntentAnnotator directory: `cd EmotionIntentAnnotator/`
3. Setup and activate a virtual environment:
   - If existing: `source venv/bin/activate` # Adjust path if venv is elsewhere
   - If new:
     - `python3 -m venv venv`
     - `source venv/bin/activate` # On Windows: venv\Scripts\activate
4. Install dependencies (if not already): `pip install -r requirements.txt` 
5. Install ffmeg (required for audio/video processing): `brew install ffmpeg` # macOS
                                                        `sudo apt-get install ffmpeg` # Ubuntu/Debian
                                                        Download from https://ffmpeg.org/download.html and add to PATH # Windows
6. Proceed to the "Run the Tool" section below.

### Run the Tool (Both Options):
1. `python3 src/setup_db.py` to initialize the database.
2. `python3 -m src.annotate_emotions` to open a GUI to:
    1. Upload a text file (e.g., data/sample_text.txt) or media file (.wav, .mp3, .m4a, .mp4, .mov):
       - Click "Upload Text", select a .txt file (e.g., data/sample_text.txt), and click "Open".
       - Click "Upload Audio/Video", select an audio or video file, and click "Open".
       - View segmented text/transcriptions (e.g., "I'm thrilled about this project! Just kidding, it's overwhelming." -> two segments); edit if needed using "Edit Text" and "Save Edit".
    2. Annotate:
       - View each segment in the GUI.
       - Click "Suggest Labels" for AI-predicted emotions.
       - Select Emotion and Intent from dropdowns.
       - Click "Save Annotation" to store in the database.
    3. Manage Annotations:
       - Use "Undo" to revert the last annotation.
       - Click "Export CSV" to save annotations as annotations_export.csv.    
3. **Optional**: To reset the database (e.g., to clear test data and start media_id at 1): mv emotions_intents.sqlite emotions_intents_backup_$(date +%F).sqlite
                                                                                           `python3 src/setup_db.py`
    
### Sample Data
The repository includes an example text file for testing text segmentation and annotation:
- **`data/sample_text.txt`**: 
  ```text
  I’m thrilled about this project! Just kidding, it’s overwhelming.
  ```
  This file is used to demonstrate the GUI’s ability to segment text into sentences and annotate emotions and intents. You can also upload your own .txt files via the GUI.

### Project Structure
- ImageAnnotationToolV2/
  - EmotionIntentAnnotator/
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

### Dependencies
- Listed in requirements.txt:
  - torch, transformers (DistilRoBERTa for emotion suggestions)
  - nltk (sentence segmentation)
  - tkinter (GUI)
  - sqlite3 (database, built-in)
  - openai-whisper, pydub

### Planned Features
- Audio Annotation: Segment and annotate WAV files using librosa.
- Video Support: Extract frames and annotate using opencv.
- Explainability: Visualize AI suggestions with SHAP or matplotlib.

### Notes
- Ensure nltk.download('punkt_tab') is run for sentence segmentation (included in process_text.py).
- The database (emotions_intents.sqlite) is created automatically by setup_db.py.
- For issues, check Python 3.8+ and virtual environment activation.

