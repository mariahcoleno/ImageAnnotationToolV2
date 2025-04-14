import sqlite3

def migrate_labels(db_path="sarcasm_db.sqlite"):
    # Hardcoded messages and labels
    hardcoded_messages = [
        ("Wow, you're SO good at this!", "Sarcastic"),
        ("I love Mondays.", "Sarcastic"),
        ("Nice weather today.", "Sarcastic")
    ]

    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    for message, label in hardcoded_messages:
        if label == "Unsure":
            continue
        new_label = "sarcastic" if label == "Sarcastic" else "non-sarcastic"

        # Check if message exists in texts
        cursor.execute("SELECT id FROM texts WHERE text_content = ?", (message,))
        result = cursor.fetchone()

        if result:
            # Message exists, get its ID
            text_id = result[0]
        else:
            # Insert new message into texts
            cursor.execute("INSERT INTO texts (text_content) VALUES (?)", (message,))
            text_id = cursor.lastrowid
            print(f"Inserted text: '{message}' with ID {text_id}")

        # Insert or update label in sarcasm_annotations
        cursor.execute("INSERT OR REPLACE INTO sarcasm_annotations (text_id, label) VALUES (?, ?)", (text_id, new_label))
        print(f"Migrated: '{message}' -> {new_label}")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    migrate_labels()
