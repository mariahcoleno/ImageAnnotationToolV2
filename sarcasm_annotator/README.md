### Sarcasm Annotation and Classification Tool
This tool annotates and classifies text for sarcasm using a Tkinter-based GUI.

### Features
- Label text as sarcastic, not sarcastic, or unsure using a Tkinter-based GUI
- Undo annotations and export to CSV
- Track progress with "Labeled: X/Y" counter
- Includes 23 predefined sample texts for immediate use
- Train a Scikit-learn logistic regression classifier with TF-IDF vectorization on labeled texts, reporting training, validation, and test accuracies.

### Screenshots
![Sarcasm Annotation Text GUI example 1](screenshots/gui_text_loaded.png)
![Sarcasm Annotation Text GUI example 2](screenshots/sarcasm_gui.png)

### Files
- `requirements.txt`: Lists all Python dependencies required to run the tool.
- `setup_sarcasm_db.py`: Initializes `sarcasm_db.sqlite` with `texts` and `sarcasm_annotations` tables, setting up the database structure.
- `load_texts.py`: Loads 20 sarcasm texts to the `sarcasm_db.sqlite` database.
- `migrate_labels.py`: A one-time migration script used to add 3 hardcoded messages to the `sarcasm_db.sqlite` database, increasing the text count to 23.  
- `sample_texts.txt`: File that contains sample sarcasm texts.
- `annotate_sarcasm.py`: The main script that runs a Tkinter-based GUI to display texts from `sarcasm_db.sqlite` and save annotations (sarcastic/not sarcastic/unsure) to the database.
- `sarcasm_db.sqlite`: Generated SQLite database storing annotations (ignored by Git).
- `sarcasm_labels.csv`: Exported CSV of labeled texts (ignored by Git).
- `train_sarcasm_classifier.py`: Trains a Scikit-learn logistic regression classifier with TF-IDF vectorization on labeled texts, reporting training, validation, and test accuracies.  Saves the trained model as `sarcasm_classifier.pkl`.
- `sarcasm_classifier.pkl`: Trained logistic regression model (generated after running training, ignored by Git).

### Requirements
- Python 3.7+ (tested with Python 3.13.3)
- Scikit-learn - for logistic regression and TF-IDF text vectorization
- NumPy - for array operations  
- Joblib - for model serialization

### Model Details
- **Algorithm**: Logistic Regression with TF-IDF vectorization
- **Features**: Up to 5,000 TF-IDF features, English stop words removed
- **Data Split**: 70% training, 15% validation, 15% testing
- **Classification**: Binary classification (Sarcastic (1) vs Not Sarcastic (0))
- **Note**: "Unsure" labels are excluded from training data

### Setup and Usage
#### Option 1: From GitHub (First Time Setup)
- **Note**:
  - Start in your preferred directory (e.g., cd ~/Desktop/ or cd ~/Downloads/ or cd ~/Documents/) to control where the repository clones. 
  - If you skip this step, it clones to your current directory.
1. Clone the repository: `git clone https://github.com/mariahcoleno/annotation-classification-toolkit.git`
2. Navigate to the sarcasm_annotator directory: `cd sarcasm_annotator/` (from the root of your cloned repository)
3. Create virtual env: `python3 -m venv venv`
4. Activate: `source venv/bin/activate`
5. Install dependencies: `pip install -r requirements.txt`
6. Proceed to the "Run the Tool" section below.

#### Option 2: Local Setup (Existing Repository):
1. Navigate to your local repository `cd ~/Documents/annotation-classification-toolkit/` # Adjust path as needed
2. Navigate to sarcasm_annotator directory: `cd sarcasm_annotator/`
3. Setup and activate a virtual environment:
   - If existing: `source venv/bin/activate` # Adjust path if venv is elsewhere
   - If new:
     - `python3 -m venv venv`
     - `source venv/bin/activate`
4. Install dependencies (if not already): `pip install -r requirements.txt` 
5. Proceed to the "Run the Tool" section below.

### Run the Tool (Both Options):
1. Create database tables: `python3 setup_sarcasm_db.py`
2. Load sample texts: `python3 load_texts.py`
3. Add additional texts: `python3 migrate_labels.py` 
4. Start the annotation GUI: `python3 annotate_sarcasm.py`
5. Using the GUI:
   - **Annotate**: Select "Sarcastic", "Not Sarcastic", or "Unsure" to label each text and automatically store annotations in a SQL database.
   - **Export**: Click "Export to CSV" to save annotations as sarcasm_labels.csv
   - **Undo**: Click "Undo" to revert the last annotation
5. Train classifier on annotations, reporting training, validation, and test accuracies: `python3 train_sarcasm_classifier.py` 

### Project Structure
- screenshots
  - gui_text_loaded.png
  - sarcasm_gui.png
- README.md
- annotate_sarcasm.py
- load_texts.py
- migrate_labels.py
- requirements.txt
- sample_texts.txt
- setup_sarcasm_db.py
- train_sarcasm_classifier.py

### Notes
- The database (`sarcasm_db.sqlite`), once populated, contains 23 texts, including 3 migrated hardcoded messages.
- The 3 hardcoded messages ("Wow, you're SO good at this!", "I love Mondays.", "Nice weather today.") were migrated once using `migrate_labels.py` and are now part of the main database.
- The tool is designed for manual annotation to support sarcasm detection models.
- "Unsure" labels in the GUI are stored, supporting flexible annotation workflows.
- Automatic loading from sample_texts.txt simplifies the user experience.

### Development Notes
- Application developed through iterative prompt engineering with AI tools (Claude/Grok) for rapid prototyping and learning.
