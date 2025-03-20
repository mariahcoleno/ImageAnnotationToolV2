# Sarcasm Annotation Tool
A Python-based workflow for labeling text snippets as sarcastic or not using a Tkinter GUI and exporting results.

## Overview
- Labels text snippets from `texts.txt` (user-provided) as "sarcastic" or "not sarcastic".
- Stores annotations in an SQLite database (`sarcasm_labels.db`).
- Exports labeled data to CSV (`sarcasm_labels.csv`) for further analysis.
- Built with Python, Tkinter, SQLite, and includes undo functionality.
- Features a responsive GUI with navigation, export, and undo options.

## Files
- `setup_sarcasm_db.py`: Initializes SQLite database (`sarcasm_labels.db`) with `texts` and `annotations` tables.
- `load_sarcasm_texts.py`: Loads text snippets from `texts.txt` into the database.
- `annotate_sarcasm.py`: Main GUI for labeling texts, with "Sarcastic", "Not Sarcastic", "Export", and "Undo" buttons.
- `sarcasm_labels.db`: SQLite database storing text IDs and labels (ignored by Git).
- `sarcasm_labels.csv`: Exported CSV of labeled texts (ignored by Git).
- `texts.txt`: Input file with text snippets, one per line (ignored by Git).

## Setup and Usage
1. **Prepare Texts**:
   - Create `texts.txt` in `sarcasm_annotation/` with one text snippet per line (e.g., "Wow, great day!" or "Yeah, because that’s *totally* believable").
   - Example:

2. **Initialize Database**:
- Run `python setup_sarcasm_db.py` to create `sarcasm_labels.db`.

3. **Load Texts**:
- Run `python load_sarcasm_texts.py` to populate the `texts` table from `texts.txt`.

4. **Annotate**:
- Run `python annotate_sarcasm.py`.
- Use "Sarcastic" or "Not Sarcastic" buttons to label each text.
- Click "Next" to move forward.
- Click "Undo" to revert the last annotation.
- Click "Export" to save all labels to `sarcasm_labels.csv`.
- GUI exits when all texts are labeled.

5. **Review**:
- Check `sarcasm_labels.csv` for exported labels (e.g., `id,text,label`).

## Database Schema
- `texts` table:
- `id INTEGER PRIMARY KEY AUTOINCREMENT`
- `text TEXT`
- `annotations` table:
- `text_id INTEGER` (foreign key to `texts.id`)
- `label TEXT` ("sarcastic" or "not sarcastic")

## Features
- **Export Button**: Saves current annotations to `sarcasm_labels.csv` at any time.
- **Undo Button**: Reverts the last annotation, updating the database and GUI.
- **Progress Tracking**: Displays "Labeled: X/Y" (e.g., "Labeled: 5/50").
- **Error Handling**: Logs issues (e.g., missing `texts.txt`) to console.

## Setup Example
```bash
echo "This is fine.\nOh, brilliant idea!" > texts.txt
python setup_sarcasm_db.py
python load_sarcasm_texts.py
python annotate_sarcasm.py


# Results - Example sarcasm_labels.csv:
id,text,label
1,"This is fine.","sarcastic"
2,"Oh, brilliant idea!","sarcastic"

Annotation accuracy depends on user judgment; no automated training yet.

# Note
Built with help from xAI's Grok to refine Tkinter GUI and SQLite integration.
Future work: Add sarcasm detection model training.
