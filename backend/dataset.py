# dataset.py
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

class QuestionDataset:
    def __init__(self, csv_path):
        self.df = pd.read_csv(csv_path)
        self.vectorizer = CountVectorizer()
        self.X = self.vectorizer.fit_transform(self.df["question"])
        self.labels = self.df["topic"].astype("category")
        self.label2id = dict(enumerate(self.labels.cat.categories))
        self.id2label = {v: k for k, v in self.label2id.items()}

    def get_dims(self):
        return self.X.shape[1], len(self.label2id)

    def decode_label(self, idx):
        return self.label2id.get(idx, "bilinmiyor")
