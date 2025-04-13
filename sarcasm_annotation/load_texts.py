import sqlite3

def load_texts(input_file, db_path="sarcasm_db.sqlite"):
    # Read texts
    with open(input_file, "r") as f:
        texts = [line.strip() for line in f if line.strip()]

    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Insert texts
    for text in texts:
        cursor.execute("INSERT OR IGNORE INTO texts (text_content) VALUES (?)", (text,))

    conn.commit()
    conn.close()
    print(f"Loaded {len(texts)} texts into {db_path}")

if __name__ == "__main__":
    load_texts("sample_texts.txt")
