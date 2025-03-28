# ImageAnnotationToolV2
## Hypothesis Annotation Tool
A Python-based tool for annotating hypotheses on images and text using a Tkinter GUI.

### Overview
- Annotates hypotheses on images (e.g., `ssc2019-15b-med.jpg`) or text with user-defined text labels.
- Stores annotations in a SQLite database and exports to CSV.
- Built with Python, Tkinter, Pillow, SQLite.
- Features interactive undo/redo for new annotations.

### Files
- `hypothesis_annotator.py`: Main script with GUI for annotating hypotheses.
- `requirements.txt`: Lists dependencies (e.g., Tkinter, Pillow).
- `images/ssc2019-15b-med.jpg`: Sample image for annotation (included in repo).
- `hypotheses.sqlite`: Generated SQLite database (ignored by Git).
- `hypothesis_data.csv`: Exported annotations (ignored by Git).

### Setup and Usage
#### Option 1: From GitHub (Clone)
- **Note**: 
  - Start in your preferred directory (e.g., `cd ~/Desktop/` or `cd ~/Documents/`) to control where the repo clones. 
  - If you skip this, it clones to your current directory.
1. Clone the repo: `git clone https://github.com/mariahcoleno/ImageAnnotationToolV2.git`
2. Navigate to hypothesis_annotator directory: `cd ImageAnnotationToolV2/hypothesis_annotator/`
3. Create a virtual environment: `python3 -m venv venv`
4. Activate the virtual environment: `source venv/bin/activate`
5. Install dependencies: `pip install -r requirements.txt`

#### Option 2: Local Setup (Existing Repo)
1. Navigate to your local repository: `cd ~/Documents/AnnotationProject/` # Adjust path as needed
2. Navigate to hypothesis_annotator directory: `cd hypothesis_annotator/`
3. Setup and activate a virtual environment:
   - If existing: `source venv/bin/activate` # Adjust path if venv is elsewhere
   - If new:
     - `python3 -m venv venv`
     - `source venv/bin/activate`
4. Install dependencies (if not already): `pip install -r requirements.txt`

### Run the Tool (Both Options):
1. `python hypothesis_annotator.py` to:
   - Open a GUI with sample entries (e.g., ssc2019-15b-med.jpg, text hypotheses).
   - Label entries as "Supported", "Refuted", or "Unsure".
   - Store annotations in a SQL database and export to CSV.
   - Use "Undo" to revert new annotations (blocked if no new actions).
              
### Results
- Annotation: Labels 3 sample hypotheses (2 text, 1 image) on first run; extensible with additional entries.
- Output: Generates hypothesis_data.csv (e.g., 380 bytes) and hypotheses.sqlite (e.g., 12KB).
- Note: GUI starts with "Labeled: X/3" based on prior labels in hypotheses.sqlite. "Undo blocked: idx=0" appears if no new actions are available to undo.

### Note
- Sample image (ssc2019-15b-med.jpg) included in `images/` for testing.
- Add your own images (e.g., from ~/Downloads, ~/Pictures/, or a dataset like NASA "Galaxies Images") to images/ (ignored by Git) and update the database to annotate them. 
  - To add new images (Images can be in various formats—not limited to .jpg (e.g., .jpg, .png, .bmp, .gif supported via Pillow)):  
    1. Copy to images/:  
       `cp /path/to/your/images/sample.png images/`
    2. Add to database:
       `sqlite3 hypotheses.sqlite "INSERT INTO hypotheses (data, modality, hypothesis) VALUES ('images/sample.png', 'image', 'Your hypothesis');"`
    - Ensure the file exists in images/ to avoid load errors (e.g., "Image load error: [Errno 2] No such file or directory").
  - To find your image path:
    - In Finder: Right-click a file, hold the Option key, select "Copy [filename] as Pathname” where [filename] is the name of your file.
    - In Terminal:
      - Navigate to your image directory: `cd ~/Downloads/` # Adjust path as needed
      - Run pwd to get the path (e.g., /Users/yourusername/Downloads/)

