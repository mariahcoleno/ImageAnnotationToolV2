# ImageAnnotationToolV2
## Hypothesis Annotation Tool
A Python-based tool for annotating hypotheses on images and text using a Tkinter GUI.

### Overview
- Annotates hypotheses on a sample image (e.g., `ssc2019-15b-med.jpg`) with user-defined text inputs.
- Stores annotations in a SQLite database and exports to CSV.
- Built with Python, Tkinter, Pillow, SQLite.
- Features interactive undo/redo functionality (with limits).

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
1.`python hypothesis_annotator.py` to:
   - open the GUI
   - view the sample image
   - add hypotheses via text input
   - save annotations (stored in hypotheses.sqlite, exported to hypothesis_data.csv).

### Note
     - Sample image (ssc2019-15b-med.jpg) included in `images/` for testing.
     - Add your own .jpg images (e.g., from ~/Downloads, ~/Pictures/, or a dataset like Nasa's "galaxy images") to images/ directory (ignored by Git) for additional annotations.
       `cp /path/to/your/images/*.jpg images/`
        - To find your path:
          - In Finder: Right-click a file, hold the Option key, select "Copy [filename] as Pathname” where [filename] is the name of your file.
          - In Terminal:
            - Navigate to your image directory: `cd ~/Downloads/` # Adjust path as needed
            - Run pwd to get the path (e.g., /Users/yourusername/Downloads/)
              - If in clone, go back to the hypothesis_annotator directory: `cd ~/ImageAnnotationToolV2/hypothesis_annotator/ (adjust if cloned elsewhere).
              
### Results
- Annotation: Successfully labels hypotheses on the sample image after user interaction.
- Output: Generates hypothesis_data.csv (e.g., 380 bytes) and hypotheses.sqlite (e.g., 12KB) with annotated data.
- Note: Undo functionality may display Undo blocked: idx=0 when no actions are available to undo—expected behavior with empty history.

