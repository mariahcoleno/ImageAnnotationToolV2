import sqlite3

def migrate_labels():
    src_conn = sqlite3.connect("sarcasm_labels.db")
    dst_conn = sqlite3.connect("sarcasm_db.sqlite")
    src_cursor = src_conn.cursor()
    dst_cursor = dst_conn.cursor()

    src_cursor.execute("SELECT message, label FROM labels")
    labels = src_cursor.fetchall()

    for message, label in labels:
        if label == "Unsure":
            continue
        new_label = "sarcastic" if label == "Sarcastic" else "non-sarcastic"

        # Check if message exists in texts
        dst_cursor.execute("SELECT id FROM texts WHERE text_content = ?", (message,))
        result = dst_cursor.fetchone()

        if result:
            # Message exists, get its ID
            text_id = result[0]
        else:
            # Insert new message into texts
            dst_cursor.execute("INSERT INTO texts (text_content) VALUES (?)", (message,))
            text_id = dst_cursor.lastrowid
            print(f"Inserted text: '{message}' with ID {text_id}")

        # Insert or update label in sarcasm_annotations
        dst_cursor.execute("INSERT OR REPLACE INTO sarcasm_annotations (text_id, label) VALUES (?, ?)", (text_id, new_label))
        print(f"Migrated: '{message}' -> {new_label}")

    dst_conn.commit()
    src_conn.close()
    dst_conn.close()

if __name__ == "__main__":
    migrate_labels()
