import sqlite3
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
import joblib

# Paths
DB_PATH = "sarcasm_db.sqlite"

# Load data from SQLite
def load_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT t.text_content, a.label
        FROM texts t
        LEFT JOIN sarcasm_annotations a ON t.id = a.text_id
        WHERE a.label IS NOT NULL
    """)
    data = cursor.fetchall()
    conn.close()

    if not data:
        print("No labeled data found.")
        return None, None

    texts, labels = [], []
    for text, label in data:
        texts.append(text)
        labels.append(1 if label == "sarcastic" else 0)

    return texts, np.array(labels)

# Main function
def main():
    # Load data
    print("Loading data...")
    texts, labels = load_data()
    if texts is None:
        return

    # Split data: 70% train, 15% val, 15% test
    X_train, X_temp, y_train, y_temp = train_test_split(
        texts, labels, test_size=0.3, random_state=42, stratify=labels
    )
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=0.5, random_state=42, stratify=y_temp
    )

    # Create pipeline: TF-IDF + Logistic Regression
    print("Training classifier...")
    pipeline = make_pipeline(
        TfidfVectorizer(max_features=5000, stop_words="english"),
        LogisticRegression(max_iter=1000, random_state=42)
    )
    pipeline.fit(X_train, y_train)

    # Evaluate
    train_acc = pipeline.score(X_train, y_train) * 100
    val_acc = pipeline.score(X_val, y_val) * 100
    test_acc = pipeline.score(X_test, y_test) * 100

    print(f"Training Accuracy: {train_acc:.2f}%")
    print(f"Validation Accuracy: {val_acc:.2f}%")
    print(f"Test Accuracy: {test_acc:.2f}%")

    # Save model
    joblib.dump(pipeline, "sarcasm_classifier.pkl")
    print("Model saved to sarcasm_classifier.pkl")

if __name__ == "__main__":
    main()
