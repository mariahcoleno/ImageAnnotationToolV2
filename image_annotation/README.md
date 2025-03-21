# ImageAnnotationToolV2
## Image Annotation Tool
A Python-based workflow for labeling images and training a PyTorch CNN to classify cats and dogs.

### Overview
- Labels 100 images (50 cats, 50 dogs) using a Tkinter GUI.
- Trains a CNN with training, validation, and test accuracies.
- Built with Python, Tkinter, Pillow, SQLite, PyTorch, Scikit-learn.
- Features 300x300 resizing during labeling; CNN uses 64x64 images.

### Files
- `setup_db.py`: Initializes SQLite database (`annotation_db.sqlite`).
- `load_images.py`: Loads images into database.
- `label_images.py`: Main labeling GUI to annotate images.
- `view_labeled.py`: Displays labeled images with "Next" button.
- `check_images.py`: Verifies labels (see also `check_db.py`).
- `export_labels.py`: Exports labels to CSV (`labeled_images.csv`).
- `verify_images.py`: Validates data integrity.
- `train_cnn_pytorch.py`: Trains PyTorch CNN on labeled data.
- `cat_dog_cnn_pytorch.pth`: Trained model weights (800KB).

### Setup and Usage
1. Clone the repo: `git clone https://github.com/mariahcoleno/ImageAnnotationToolV2.git`
2. Create virtual env: `python3 -m venv venv`
3. Activate: `source venv/bin/activate`
4. Navigate: `cd image_annotation/`
5. Install dependencies: `pip install -r requirements.txt`
6. Place images in `images/` (ignored by Git):
   - `mkdir images`
   - Add .jpg files (e.g., copy your own: `cp /path/to/your/images/*.jpg images/`).
7. Run:
   - `python setup_db.py` to initialize the database.
   - `python load_images.py` to load images.
   - `python label_images.py` to label images.
   - `python view_labeled.py` to view labeled images.
   - `python train_cnn_pytorch.py` to train the CNN (after labeling).

### Results
- Annotation: 100% user accuracy after 5+ hours of debugging.
- CNN (10 epochs):
  - Training Accuracy: ~70% (64 images).
  - Validation Accuracy: ~62% (16 images).
  - Test Accuracy: 50% (20 images, small dataset).

### Note
- PyTorch CNN code adapted from xAI's Grok as I learn PyTorch.
