# Bounding Box Annotation Tool
A Python-based tool for annotating images with bounding boxes using a Tkinter GUI.

## Overview
- Annotates images by drawing bounding boxes and assigning labels.
- Stores annotations in SQLite; exports to CSV.
- Built with Python, Tkinter, Pillow, SQLite.

## Files
- `setup_db.py`: Initializes SQLite database (`bounding_box_db.sqlite`).
- `load_images.py`: Loads images from `images/` into database.
- `annotate_boxes.py`: GUI to draw boxes and label objects.
- `export_boxes.py`: Exports annotations to `bounding_boxes.csv`.

## Setup and Usage
1. Navigate to directory:
   ```bash
   cd ~/Documents/AnnotationProject/bounding_box_annotation/
