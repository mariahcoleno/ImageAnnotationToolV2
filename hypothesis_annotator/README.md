## Hypothesis Annotation Tool
This tool annotates text hypotheses with or without corresponding images using a Tkinter-based GUI.

### Features
- Label hypotheses as supported, refuted, or unsure using a Tkinter-based GUI
- Undo and save annotations with export to CSV functionality

### Screenshots
![Text Hypothesis GUI](screenshots/Text_hypothesis_GUI.png)
![Image Hypothesis GUI](screenshots/Image_hypothesis_GUI.png)

### Files
- `hypothesis_annotator.py`: Main script with GUI for annotating hypotheses.
- `requirements.txt`: Lists all Python dependencies required to run the tool.
- `images/ssc2019-15b-med.jpg`: Sample image for annotation (included in repo).
- `hypotheses.sqlite`: Generated SQLite database storing annoations 09[987[.(ignored by Git).
- `hypothesis_data.csv`: Exported annotations (ignored by Git).

### Requirements
- Python 3.7+ (tested with Python 3.13.3)
- Pillow (PIL) - for image processing

### Setup and Usage
#### Option 1: From GitHub (First Time Setup)
- **Note**: 
  - Start in your preferred directory (e.g., `cd ~/Desktop/` or `cd ~/Downloads/` or `cd ~/Documents/`) to control where the repository clones. 
  - If you skip this step, it clones to your current directory.
1. Clone the repository: `git clone https://github.com/mariahcoleno/annotation-classification-toolkit.git`
2. Navigate to the hypothesis_annotator directory: `cd hypothesis_annotator/` (from the root of your cloned repository)
3. Create a virtual environment: `python3 -m venv venv`
4. Activate the virtual environment: `source venv/bin/activate`
5. Install dependencies: `pip install -r requirements.txt`
6. Proceed to the "Run the Tool" section below.

#### Option 2: Local Setup (Existing Repository)
1. Navigate to your local repository: `cd ~/Documents/annotation-classification-toolkit/` # Adjust path as needed
2. Navigate to hypothesis_annotator directory: `cd hypothesis_annotator/`
3. Setup and activate a virtual environment:
   - If existing: `source venv/bin/activate` # Adjust path if venv is elsewhere
   - If new:
     - `python3 -m venv venv`
     - `source venv/bin/activate`
4. Install dependencies (if not already): `pip install -r requirements.txt`
5. Proceed to the "Run the Tool" section below.

### Run the Tool (Both Options):
1. `python3 hypothesis_annotator.py` to:
   - Open a GUI with sample entries (e.g., ssc2019-15b-med.jpg, text hypotheses).
   - Label entries as "Supported", "Refuted", or "Unsure".
   - Store annotations in a SQL database and export to CSV.
   - Use "Undo" to revert new annotations (blocked if no new actions).
   - **Note**: To annotate your own images, see Tips below.
              
### Results
- Annotation: Labels 3 sample hypotheses (2 text, 1 image) on first run; extensible with additional entries.
- Output: Generates `hypothesis_data.csv` (e.g., 380 bytes) and `hypotheses.sqlite` (e.g., 12KB).
- Note: GUI starts with "Labeled: X/3" based on prior labels in `hypotheses.sqlite`. "Undo blocked: idx=0" appears if no new actions are available to undo.

### Project Structure
- annotation-classification-toolkit/
  - hypothesis_annotator/
    - images
      - galaxy.jpg
      - ssc2019-15b-med.jpg
    - screenshots
      - Image_hypothesis_GUI.png
      - Text_hypothesis_GUI.png
    - README.md
    - hypothesis_annotator.py  
    - requirements.txt
  - .gitignore
  - README.md

### Tips
- To annotate your own images:
  1. Add your own images (e.g., from ~/Downloads, ~/Pictures/, or a dataset like NASA "Galaxies Images") to images/: `cp /path/to/your/images/sample.png images/`
     - **Note**:
       - Images can be in various formats supported by Pillow (e.g., `.jpg`, `.png`, `.bmp`, `.gif`)
       - To find your image path and copy your images to `images/`:
         - Option 1: Use a Separate Terminal
           - Open a new terminal window or tab.
           - Navigate to your images directory: `cd ~/Downloads/` (adjust as needed).
           - Run `pwd` to get the path, e.g., `/Users/yourusername/Downloads/`.
           - Copy that path. Then go back to your original terminal (still in hypothesis_annotation/), and use it in the cp command.
         - Option 2: Use your File Explorer
           - On macOS, right-click a file in Finder, hold the Option key, and select "Copy [filename] as Pathname" to get the full path (e.g., /Users/yourusername/Downloads/image1.jpg). Remove the filename to get the directory path.
           - On Windows or Linux, you can drag the folder into the terminal to see its path.
           - Use that path in the cp command without leaving `hypothesis_annotator/`.
         - Option 3: Type the Path Directly
           - If you already know where your images are (e.g., ~/Downloads/), just use that in the cp command.
           - You can also start typing the path in the terminal and use tab completion to fill it in.
  2. Add your images to the database:
     - Open SQLite terminal: `sqlite3 hypotheses.sqlite`
     - At the sqlite> prompt: `"INSERT INTO hypotheses (data, modality, hypothesis) VALUES ('images/sample.png', 'image', 'Your hypothesis');"`
  3. Proceed to the "Run the Tool" section above.

### Development Notes
- Application developed through iterative prompt engineering with AI tools (Claude/Grok) for rapid prototyping and learning.
