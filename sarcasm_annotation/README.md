# Sarcasm Detection Annotation Tool
A Python-based tool for labeling text snippets as "Sarcastic," "Not Sarcastic," or "Maybe" for NLP tasks.

## Overview
- Labels short texts using a Tkinter GUI.
- Stores annotations in SQLite.
- Built with Python, Tkinter, SQLite.
- Features a progress counter (e.g., "Labeled: X/Y"), undo option, and CSV export.

## Files
- `setup_sarcasm_db.py`: Initialize SQLite database (`sarcasm_db.sqlite`).
- `load_sarcasm_texts.py`: Load texts from `texts.txt`.
- `annotate_sarcasm.py`: Main labeling GUI with "Maybe" and "Undo".
- `view_sarcasm_labels.py`: View labeled texts.
- `export_sarcasm_labels.py`: Export annotations to `sarcasm_labels.csv`.

## Setup and Usage
1. Create or edit `texts.txt` with one text snippet per line (e.g., "This is great weather").
2. Run `python setup_sarcasm_db.py` to reset and initialize the database.
3. Load texts with `python load_sarcasm_texts.py`.
4. Label texts with `python annotate_sarcasm.py` (use "Maybe" for uncertain cases; "Undo" to revert).
5. Export labels with `python export_sarcasm_labels.py`.
6. View annotations with `python view_sarcasm_labels.py`.

## Sample Texts
- Included in `texts.txt`:
  - "Wow, you're *so* good at this game." (Sarcastic)
  - "I love waiting an hour for my food." (Sarcastic)
  - "The weather is just perfect today." (Not Sarcastic?)
- Add your own texts to `texts.txt`.

## Output
- `sarcasm_labels.csv`: Contains labeled data in `text,label` format, ready for NLP model training.

