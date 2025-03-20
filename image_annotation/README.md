# Image Annotation Tool
A Python-based workflow for labeling images and training a PyTorch CNN to classify cats and dogs.

## Overview
- Labels 100 images (50 cats, 50 dogs) using a Tkinter GUI.
- Trains a CNN with training, validation, and test accuracies.
- Built with Python, Tkinter, Pillow, SQLite, PyTorch, Scikit-learn.
- Features 300x300 resizing during labeling; CNN uses 64x64 images.

## Files
- `setup_db.py`: Initializes SQLite database (`annotation_db.sqlite`).
- `load_images.py`: Loads images into database.
- `label_images.py`: Main labeling GUI to annotate images.
- `view_labeled.py`: Displays labeled images with "Next" button.
- `check_images.py`: Verifies labels (see also `check_db.py`).
- `export_labels.py`: Exports labels to CSV (`labeled_images.csv`).
- `verify_images.py`: Validates data integrity.
- `train_cnn_pytorch.py`: Trains PyTorch CNN on labeled data.
- `cat_dog_cnn_pytorch.pth`: Trained model weights (800KB).

## Setup and Usage
1. Place images in `images/` (ignored by Git).
2. Run `python setup_db.py` and `python load_images.py`.
3. Label with `python label_images.py`.
4. View with `python view_labeled.py`.
5. Train with `python train_cnn_pytorch.py`.

## Results
- Annotation: 100% user accuracy after 5+ hours of debugging.
- CNN (10 epochs):
  - Training Accuracy: ~70% (64 images).
  - Validation Accuracy: ~62% (16 images).
  - Test Accuracy: 50% (20 images, small dataset).

## Note
- PyTorch CNN code adapted from xAI's Grok as I learn PyTorch.
