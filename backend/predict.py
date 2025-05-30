# predict.py
import torch
from dataset import QuestionDataset
from model import SimpleClassifier

# Aynı veri seti ve model
dataset = QuestionDataset("questions.csv")
input_dim, output_dim = dataset.get_dims()
model = SimpleClassifier(input_dim, output_dim)
model.load_state_dict(torch.load("model.pth"))  # Eğer kaydettiysen

# Eğitmeden direkt kullanıyorsan:
model.eval()

def predict(text):
    x = dataset.vectorizer.transform([text]).toarray()
    x_tensor = torch.tensor(x[0], dtype=torch.float32)
    with torch.no_grad():
        logits = model(x_tensor)
        predicted_class = torch.argmax(logits).item()
        return dataset.decode_label(predicted_class)

# Örnek tahmin
soru = "Bu parçada anlatılmak istenen nedir?"
print(f"Soru: {soru}")
print(f"Tahmin edilen konu: {predict(soru)}")
