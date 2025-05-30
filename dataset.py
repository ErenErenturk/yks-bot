# dataset.py
import torch
from torch.utils.data import Dataset
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

class QuestionDataset(Dataset):
    def __init__(self, csv_path):
        self.df = pd.read_csv(csv_path)
        self.vectorizer = TfidfVectorizer()
        self.X = self.vectorizer.fit_transform(self.df['question']).toarray()

        self.encoder = LabelEncoder()
        self.y = self.encoder.fit_transform(self.df['topic'])

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        return torch.tensor(self.X[idx], dtype=torch.float32), torch.tensor(self.y[idx], dtype=torch.long)

    def get_dims(self):
        return self.X.shape[1], len(self.encoder.classes_)

    def decode_label(self, idx):
        return self.encoder.inverse_transform([idx])[0]
