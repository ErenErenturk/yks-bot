# train.py
import torch
import torch.nn as nn
from model import SimpleClassifier
from dataset import QuestionDataset

# Veri kümesini yükle
dataset = QuestionDataset("questions.csv")
X = dataset.X.toarray()
y = dataset.labels.cat.codes.values

# Tensor'lara çevir
X_tensor = torch.tensor(X, dtype=torch.float32)
y_tensor = torch.tensor(y, dtype=torch.long)

# Model ve loss/optimizer
input_dim, output_dim = dataset.get_dims()
model = SimpleClassifier(input_dim, output_dim)
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

# Eğitim
for epoch in range(10):
    optimizer.zero_grad()
    outputs = model(X_tensor)
    loss = criterion(outputs, y_tensor)
    loss.backward()
    optimizer.step()

    preds = torch.argmax(outputs, dim=1)
    accuracy = (preds == y_tensor).float().mean().item()
    print(f"Epoch {epoch+1} | Loss: {loss.item():.4f} | Accuracy: {accuracy:.2f}")

# Modeli kaydet
torch.save(model.state_dict(), "model.pth")
