# ImageAnnotationToolV2
## Image Annotation Tool
A Python-based workflow for labeling images and training a PyTorch CNN to classify cats and dogs.

### Overview
- Labels 100 images (50 cats, 50 dogs) using a Tkinter GUI.
- Trains a CNN with training, validation, and test accuracies.
- Built with Python, Tkinter, Pillow, SQLite, PyTorch, Scikit-learn.
- Features 300x300 resizing during labeling; CNN uses 64x64 images.

### Files
- `requirements.txt`: Lists dependencies (e.g., Pillow, torch, numpy, etc.) required to run the scripts.
- `setup_db.py`: Initializes SQLite database (`annotation_db.sqlite`).
- `load_images.py`: Loads images into database.
- `label_images.py`: Main script for labeling images.
- `view_labeled.py`: Script to view labeled images.
- `images/`: Directory for input images (e.g., example.jpg)
- `check_images.py`: Verifies labels (see also `check_db.py`).
- `export_labels.py`: Exports labels to CSV (`labeled_images.csv`).
- `verify_images.py`: Validates data integrity.
- `train_cnn_pytorch.py`: Trains PyTorch CNN on labeled data.
- `cat_dog_cnn_pytorch.pth`: Trained model weights (800KB).
- `annotation_db.sqlite`: Generated SQLite database storing annotations (ignored by Git)
- `labeled_images.csv`: Exported labeled image data (ignored by Git)

### Setup and Usage
#### Option 1: From GitHub (Clone)
- **Note**: 
  - Start in your preferred directory (e.g., `cd ~/Desktop/` or `cd ~/Documents/`) to control where the repo clones. 
  - If you skip this, it clones to your current directory.
1. Clone the repo: `git clone https://github.com/mariahcoleno/ImageAnnotationToolV2.git`
2. Navigate to image_annotation directory: `cd ImageAnnotationToolV2/image_annotation/`
3. Create a virtual environment: `python3 -m venv venv`
4. Activate the virtual environment: `source venv/bin/activate`
5. Install dependencies: `pip install -r requirements.txt`
6. Place images in `images/` (ignored by Git):
   - `mkdir -p images/`
   - `cp /path/to/your/images/*.jpg images/`
   - **Note**: 
     - This repo does not include sample images.
     - Use your own .jpg files (e.g., from ~/Downloads/, ~/Pictures/, or a dataset like Kaggle’s “Cats vs Dogs”). 
     - To find your path:
       - In Finder: Right-click a file, hold the Option key, select "Copy [filename] as Pathname” where [filename] is the name of your file. 
       - In Terminal:
         - Navigate to your image directory: `cd ~/Downloads/` # Adjust path as needed
         - Run pwd to get the path (e.g., /Users/yourusername/Downloads/)
         - Go back to the image_annotation directory: `cd ~/ImageAnnotationToolV2/image_annotation/` (adjust if cloned elsewhere).

#### Option 2: Local Setup (Existing Repo)
1. Navigate to your local repository: `cd ~/Documents/AnnotationProject/` # Adjust path as needed
2. Navigate to image_annotation directory: `cd image_annotation/`
3. Setup and activate a virtual environment:
   - If existing: `source venv/bin/activate` # Adjust path if venv is elsewhere
   - If new:
     - `python3 -m venv venv`
     - `source venv/bin/activate`
4. Install dependencies (if not already): `pip install -r requirements.txt`
5. Place images in the images/ directory (ignored by Git): 
   - `mkdir -p images/`
   - `cp /path/to/your/images/*.jpg images/`

### Run the Tool (Both Options):
1. `python setup_db.py` to initialize the database.
2. `python load_images.py` to load images.
3. `python label_images.py` to label images.
4. `python view_labeled.py` to view labeled images.
5. `python export_labels.py` to export annotations to labeled_images.csv
6. `python train_cnn_pytorch.py` to train the CNN (after labeling).

### Results
- Annotation: 100% user accuracy after 5+ hours of debugging.
- CNN (10 epochs):
  - Training Accuracy: ~100% (80 images).
  - Validation Accuracy: ~100% (10 images).
  - Test Accuracy: 70% (10 images, small dataset).

### Note
- PyTorch CNN code adapted from xAI's Grok as I learn PyTorch.
- Results based on 100 labeled images; expect variance with small test set (10 images).
