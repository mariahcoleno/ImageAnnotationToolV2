# ImageAnnotationToolV2 
## Bounding Box Annotation Tool
A Python-based tool for annotating images with bounding boxes using a Tkinter GUI.

### Overview
- Annotates images by drawing bounding boxes and assigning labels.
- Stores annotations in SQLite; exports to CSV.
- Built with Python, Tkinter, Pillow, SQLite.

### Files
- `requirements.txt`: Lists dependencies (e.g. Pillow) required to run the scripts.
- `setup_db.py`: Initializes SQLite database (`bounding_box_db.sqlite`).
- `load_images.py`: Loads images from `images/` into database.
- `annotate_boxes.py`: GUI to draw boxes and label objects.
- `export_boxes.py`: Exports annotations to `bounding_boxes.csv`.
- `bounding_box_db.sqlite`: Generated SQLite database (ignored by Git).
- `bounding_boxes.csv`: Exported annotations (ignored by Git).

### Setup and Usage 
#### Option 1: From GitHub(Clone)
- **Note**:
  - Start in your preferred directory (e.g., cd ~/Desktop/ or cd ~/Downloads/ or cd ~/Documents/) to control where the repository clones.
  - If you skip this, it clones to your current directory.
1. Clone the repository: `git clone https://github.com/mariahcoleno/ImageAnnotationToolV2.git`                                      
2. Navigate to the bounding_box_annotation directory: `cd bounding_box_annotation/` (from the root of your cloned repository)
3. Create virtual environment: `python3 -m venv venv`
4. Activate virtual environment (from parent dir): `source venv/bin/activate`
5. Install dependencies: `pip install -r requirements.txt`
6. Use existing images from `..image_annotation/images/` (shared directory):
   - Ensure images are in `../image_annotation/images/` (e.g., from image_annotation setup).
   - Or add new images to shared directory:  
     - `mkdir -p ../image_annotation/images/` (if doesn't already exist)
     - `cp /path/to/your/images/*.jpg ../image_annotation/images/`
     - **Note**:
       - This repository shares sample images with the image_annotation tool.
       - If images don't already exist in `..image_annoation/images/`, use your own .jpg files (e.g. from ~/Downloads/, ~/Pictures/, or a dataset like Kaggle's "Cats vs Dogs").
       - To find your path:
         - In Finder: Right-click a file, hold the Option key, select "Copy [filename] as Pathname" where [filename] is the name of your file.
         - In Terminal:
           - Navigate to your image directory: cd ~/Downloads/ # Adjust path as needed
           - Run 'pwd' to get the path (e.g., /Users/yourusername/Downloads/).
           - Return to the ..image_annotation/images/ directory: cd image_annotation/images/ (from the root of your clone repository)

#### Option 2: Local Setup (Existing Repository)
1. Navigate to your local repository: `cd ~/Documents/AnnotationProject/` # Adjust path as needed
2. Navigate to the bounding_box_annotation directory: `cd bounding_box_annotation/`
3. Setup and activate a virtual environment:
   - If existing: `source venv/bin/activate` # Adjust path if venv is elsewhere
   - If new: 
     - `python3 -m venv venv`
     - `source venv/bin/activate`
4. Install dependencies (if not already): `pip install -r requirements.txt`

5. Use existing images from `..image_annotation/images/` (shared directory):
   - Ensure images are in `../image_annotation/images/` (e.g., from image_annotation setup).
   - Or add new images to shared directory:
     - `mkdir -p ../image_annotation/images/` (if doesn't already exist)
     - `cp /path/to/your/images/*.jpg ../image_annotation/images/`

### Run the Tool (Both Options):
1. `python setup_db.py` to initialize the database.
2. `python load_images.py` to load images from ../image_annotation/images/.
3. `python annotate_boxes.py` to draw bounding boxes and label objects.
4. `python export_boxes.py` to export annotations to bounding_boxes.csv.

### Results
-Example Output (bounding_boxes.csv):
 file_path,x1,y1,x2,y2,label
 ../image_annotation/images/cat.6.jpg,70,222,301,459,Cat box
 ../image_annotation/images/dog.36.jpg,107,90,473,535,Dog box 

### Notes
- Shares `images/` with `image_annotation/`—ensure images are present in `../image_annotation/images/`.
- Example: Draw boxes around "cat" or "dog" and assign labels.

