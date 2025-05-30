# train.py
import torch
from torch.utils.data import DataLoader
import torch.nn.functional as F
from torch.optim import Adam
from dataset import QuestionDataset
from model import SimpleClassifier

# Veri ve model
dataset = QuestionDataset("questions_retrained.csv")
input_dim, output_dim = dataset.get_dims()
model = SimpleClassifier(input_dim, output_dim)

dataloader = DataLoader(dataset, batch_size=4, shuffle=True)
optimizer = Adam(model.parameters(), lr=0.01)

# Eğitim
for epoch in range(10):
    total_loss = 0
    correct = 0
    for x, y in dataloader:
        logits = model(x)
        loss = F.cross_entropy(logits, y)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_loss += loss.item()
        correct += (logits.argmax(dim=1) == y).sum().item()

    print(f"Epoch {epoch+1} | Loss: {total_loss:.4f} | Accuracy: {correct/len(dataset):.2f}")

# Modeli kaydet
torch.save(model.state_dict(), "model.pth")
