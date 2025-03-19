# Sarcasm Detection Annotation Tool
A Python-based tool for labeling text snippets as "Sarcastic" or "Not Sarcastic" for NLP tasks.

## Overview
- Labels short texts using a Tkinter GUI.
- Stores annotations in SQLite.
- Built with Python, Tkinter, SQLite.
- Features a progress counter (e.g., "Labeled: X/Y").

## Files
- `setup_sarcasm_db.py`: Initialize SQLite database (`sarcasm_db.sqlite`).
- `load_sarcasm_texts.py`: Load sample texts.
- `annotate_sarcasm.py`: Main labeling GUI.
- `view_sarcasm_labels.py`: View labeled texts.

## Setup and Usage
1. Run `python setup_sarcasm_db.py`.
2. Load texts with `python load_sarcasm_texts.py` (edit for custom texts).
3. Label with `python annotate_sarcasm.py`.
4. View with `python view_sarcasm_labels.py`.

## Sample Texts
- "Wow, you're *so* good at this game." (Sarcastic)
- "The weather is just perfect today." (Not Sarcastic?)
- Add your own in `load_sarcasm_texts.py`.
