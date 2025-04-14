import sqlite3
import os

def load_texts(input_file, db_path="sarcasm_db.sqlite"):
    # Check if input file exists
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file '{input_file}' not found")

    # Read texts
    with open(input_file, "r") as f:
        texts = [line.strip() for line in f if line.strip()]

    if not texts:
        print(f"No valid texts found in '{input_file}'")
        return

    # Connect to database
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Verify texts table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='texts'")
        if not cursor.fetchone():
            raise sqlite3.OperationalError("Table 'texts' does not exist. Run setup_sarcasm_db.py first")

        # Insert texts
        inserted = 0
        for text in texts:
            cursor.execute("INSERT OR IGNORE INTO texts (text_content) VALUES (?)", (text,))
            inserted += cursor.rowcount

        conn.commit()
        print(f"Loaded {inserted} new texts into {db_path} (from {len(texts)} in file)")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    try:
        load_texts("sample_texts.txt")
    except Exception as e:
        print(f"Error: {e}")
