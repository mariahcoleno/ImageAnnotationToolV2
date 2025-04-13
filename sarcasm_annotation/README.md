# ImageAnnotationToolV2
### Sarcasm Annotation Tool
A Tkinter GUI for labeling text as sarcastic or non-sarcastic, with undo and CSV export functionality. Trains a Scikit-learn logistic regression classifier on labeled texts, reporting training, validation, and test accuracies. Built with Python, Tkinter, SQLite (with PRAGMA foreign_keys, ON DELETE CASCADE), and Scikit-learn.

### Overview
- Labels text as sarcastic or non-sarcastic with a user-friendly GUI.
- Supports undoing annotations and exporting to CSV.
- Stores texts and annotations in SQLite with robust constraints.
- Trains a text classifier to predict sarcasm using TF-IDF features.

### Screenshots

![Sarcasm Annotation Text GUI example 1](screenshots/gui_text_loaded.png)
![Sarcasm Annotation Text GUI example 2](screenshots/sarcasm_gui.png)

### Files
- `requirements.txt`: Lists dependencies required to run scripts.
- `setup_sarcasm_db.py`: Sets up the database.
- `load_texts.py`: Loads sarcasm texts to the database.
- `sample_texts.txt`: File that contains sample sarcasm texts.
- `annotate_sarcasm.py`: Main script containing the GUI, database setup, and labeling logic.
- `sarcasm_db.sqlite`: Generated SQLite database storing labeled texts (ignored by Git).
- `sarcasm_labels.csv`: Exported CSV of labeled texts (ignored by Git).
- `train_sarcasm_classifier.py`: Trains a classifier on labeled texts, reporting training, validation, and test accuracies.

### Setup and Usage
#### Option 1: From GitHub (Clone)
- **Note**:
  - Start in your preferred directory (e.g., cd ~/Desktop/ or cd ~/Downloads/ or cd ~/Documents/) to control where the repository clones. 
  - If you skip this step, it clones to your current directory.
1. Clone the repository: `git clone https://github.com/mariahcoleno/ImageAnnotationToolV2.git`
2. Navigate to the sarcasm_annotation directory: `cd sarcasm_annotation/` (from the root of your cloned repository)
3. Create virtual env: `python3 -m venv venv`
4. Activate: `source venv/bin/activate`
5. Install dependencies: `pip install -r requirements.txt`  # No external dependencies needed
6. Proceed to the "Run the Tool" section below.

#### Option 2: Local Setup (Existing Repository):
1. Navigate to your local repository `cd ~/Documents/AnnotationProject/` # Adjust path as needed
2. Navigate to sarcasm_annotation directory: `cd sarcasm_annotation/`
3. Setup and activate a virtual environment:
   - If existing: `source venv/bin/activate` # Adjust path if venv is elsewhere
   - If new:
     - `python3 -m venv venv`
     - `source venv/bin/activate`
4. Install dependencies (if not already): `pip install -r requirements.txt` 
5. Proceed to the "Run the Tool" section below.

### Run the Tool (Both Options):
1. `python annotate_sarcasm.py` to:
   - Open a GUI with sample entries.
   - Use "Sarcastic", "Not Sarcastic", or "Unsure" buttons to label each text. 
   - Store annotations in a SQL database and export to CSV.
   - Click "Undo" to revert the last annotation.

### Results
- Annotation: Labels 3 text snippets as Sarcastic, Not Sarcastic, or Unsure.
- Output: Generates sarcasm_labels.csv and sarcasm_labels.db.
- Note: GUI starts with "Labeled: 0/3".

### Database Schema
- **labels table**:
  - `id INTEGER PRIMARY KEY AUTOINCREMENT`
  - `message TEXT`
  - `label TEXT` ("Sarcastic", "Not Sarcastic", or "Unsure")

### Features
- **Export to CSV Button**: Saves all current annotations to `sarcasm_labels.csv` at any time.
- **Undo Button**: Reverts the last annotation, updating the database and GUI.
- **Progress Tracking**: Displays "Labeled: X/Y" (e.g., "Labeled: 2/3").
- **Predefined Texts**:  No external `texts.txt` required.
