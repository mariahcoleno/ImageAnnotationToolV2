## Sarcasm Annotation Tool
A Python-based workflow for labeling text snippets as sarcastic or not using a Tkinter GUI and exporting results.

### Overview
- Labels predefined text snippets as "Sarcastic", "Not Sarcastic", or "Unsure".
- Stores annotations in an SQLite database (`sarcasm_labels.db`).
- Exports labeled data to CSV (`sarcasm_labels.csv`) for further analysis.
- Built with Python, Tkinter, SQLite, and includes undo functionality.
- Features a responsive GUI with labeling, export, and undo options.

### Files
- `annotate_sarcasm.py`: Main script containing the GUI, database setup, and labeling logic.
- `sarcasm_labels.db`: SQLite database storing labeled texts (ignored by Git).
- `sarcasm_labels.csv`: Exported CSV of labeled texts (ignored by Git).

### Setup and Usage
#### Option 1: From GitHub (Clone)
1. Clone the repo: `git clone https://github.com/mariahcoleno/ImageAnnotationToolV2.git`
2. Navigate to sarcasm_annotation directory: `cd ImageAnnotationToolV2/sarcasm_annotation/`
3. Create virtual env: `python3 -m venv venv`
4. Activate: `source venv/bin/activate`
5. Install dependencies: `pip install -r requirements.txt`  # No external dependencies needed

#### Option 2: Local Setup (Existing Repo):
1. Navigate to your local repository `cd ~/Documents/AnnotationProject/` # Adjust path as needed
2. Navigate to sarcasm_annoation directory: `cd sarcasm_annotation/`
3. Setup and activate a virtual environment:
   - If existing: `source venv/bin/activate` # Adjust path if venv is elsewhere
   - If new:
     - `python3 -m venv venv`
     - `source venv/bin/activate`
4. Install dependencies (if not already): `pip install -r requirements.txt` 

### Run the Tool (Both Options):
1. `python annotate_sarcasm.py`
   - Use "Sarcastic", "Not Sarcastic", or "Unsure" buttons to label each text. 
   - Click "Undo" to revert the last annotation.
   - Click "Export to CSV" to save labels to `sarcasm_labels.csv`.
   - GUI exits when all 3 predefined texts are labeled.

### Database Schema
- **labels table**:
  - `id INTEGER PRIMARY KEY AUTOINCREMENT`
  - `message TEXT`
  - `label TEXT` ("Sarcastic", "Not Sarcastic", or "Unsure")

### Features
- **Export Button**: Saves all current annotations to `sarcasm_labels.csv` at any time.
- **Undo Button**: Reverts the last annotation, updating the database and GUI.
- **Progress Tracking**: Displays "Labeled: X/Y" (e.g., "Labeled: 2/3").
- **Predefined Texts**: Currently hardcoded (3 examples); no external `texts.txt` required.

### Setup Example
```bash
cd sarcasm_annotation/
python annotate_sarcasm.py
