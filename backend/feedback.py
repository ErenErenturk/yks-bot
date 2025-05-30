# feedback.py
import csv
import os

FEEDBACK_FILE = "feedback.csv"

def save_feedback(question: str, topic: str, is_correct: bool):
    file_exists = os.path.isfile(FEEDBACK_FILE)
    with open(FEEDBACK_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["question", "topic", "is_correct"])
        writer.writerow([question, topic, is_correct])
