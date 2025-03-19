# Annotation Workflow Toolkit
A collection of Python-based annotation tools for machine learning datasets, developed with assistance from xAI's Grok to showcase my growing skills.

## Overview
This repository contains two distinct annotation workflows:
- **Image Annotation Tool**: Labels images (e.g., cats and dogs) and trains a PyTorch CNN.
- **Sarcasm Detection Annotation Tool**: Labels text snippets for sarcasm detection in NLP.

## Tools
### 1. Image Annotation Tool
- **Path**: `image_annotation/`
- **Purpose**: Labels 100 images (50 cats, 50 dogs) with a Tkinter GUI, then trains a CNN to classify them.
- **Details**: See `image_annotation/README.md`.

### 2. Sarcasm Detection Annotation Tool
- **Path**: `sarcasm_annotation/`
- **Purpose**: Labels text snippets as "Sarcastic" or "Not Sarcastic" for NLP tasks.
- **Details**: See `sarcasm_annotation/README.md`.

## Usage
- Each tool has its own subdirectory with scripts and instructions.
- Built with Python, Tkinter, SQLite, and PyTorch (for image tool).
- See sub-READMEs for setup and running instructions.

## Note
As a learning project, I adapted some code (e.g., PyTorch CNN) from xAI's Grok while building my own annotation pipelines.
