# ImageAnnotationToolV2 
## Bounding Box Annotation Tool
A Python-based tool for annotating images with bounding boxes using a Tkinter GUI.

### Overview
- Annotates images by drawing bounding boxes and assigning labels.
- Stores annotations in SQLite; exports to CSV.
- Built with Python, Tkinter, Pillow, SQLite.

### Files
- `setup_db.py`: Initializes SQLite database (`bounding_box_db.sqlite`).
- `load_images.py`: Loads images from `images/` into database.
- `annotate_boxes.py`: GUI to draw boxes and label objects.
- `export_boxes.py`: Exports annotations to `bounding_boxes.csv`.

### Setup and Usage
1. Clone the repo (if not already done): `git clone https://github.com/mariahcoleno/ImageAnnotationToolV2.git`
                                         
2. Create virtual env: `python3 -m venv venv`

3. Activate virtual environment (from parent dir): `source venv/bin/activate`

4. Navigate: `cd ImageAnnotationToolV2/bounding_box_annotation/`

5. Install dependencies: `pip install -r requirements.txt`

6. Use existing images from `image_annotation/` (shared directory):
   - Ensure images are in `../image_annotation/images/` (e.g., from image_annotation setup).
   - Or add new images:  
     - `mkdir -p ../image_annotation/images/`
     - Add.jpg files (e.g., copy your own: `cp /path/to/your/images/*.jpg ../image_annotation/images/`).

7. Run:
   - `python setup_db.py` to initialize the database.
   - `python load_images.py` to load images from ../image_annotation/images/.
   - `python annotate_boxes.py` to draw bounding boxes and label objects.
   - `python export_boxes.py` to export annotations to bounding_boxes.

### Notes
- Shares `images/` with `image_annotation/`—ensure images are present in `../image_annotation/images/`.
- Example: Draw boxes around "cat" or "dog" and assign labels.

