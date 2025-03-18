# Image Annotation and Classification Tool
A Python-based workflow for labeling images and training a PyTorch CNN to classify cats and dogs, built as a learning project with help from xAI's Grok.

## Overview
- **Annotation**: Labeled 100 images (50 cats, 50 dogs) using a Tkinter GUI, stored in an SQLite database after 5+ hours of debugging for accuracy.
- **Training**: Trained a simple PyTorch CNN on the labeled dataset to compute training, validation, and test accuracies.
- **Tools**: Python, Tkinter, Pillow, SQLite, PyTorch, Scikit-learn.
- **Features**:
  - GUI resizes images to 300x300 for labeling.
  - CNN processes 64x64 images, achieving ~50% test accuracy (small dataset).
- **Learning Note**: As a PyTorch beginner, I adapted the CNN training code from xAI's Grok to learn PyTorch while applying it to my custom dataset.

## Files
- **Annotation**:
  - `label_images.py`: Main labeling GUI.
  - `view_labeled.py`: View labeled images.
  - `check_images.py`: Verify labels.
  - `export_labels.py`: Export to CSV.
  - `load_images.py`: Load images to DB.
  - `setup_db.py`: Initialize database.
  - `verify_images.py`: Validate data integrity.
- **Training**:
  - `train_cnn.py`: PyTorch script to train CNN and report accuracies.
  - `cat_dog_cnn_pytorch.pth`: Trained model weights (800KB).

## Results
- **Annotation**: Successfully labeled 100 images with 100% user accuracy via GUI.
- **Training**: CNN results after 10 epochs:
  - Training Accuracy: ~70% (64 images).
  - Validation Accuracy: ~62% (16 images).
  - Test Accuracy: 50% (20 images, expected due to small dataset).
