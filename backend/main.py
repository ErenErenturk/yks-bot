from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from PIL import Image
import pytesseract
import torch
import io

from model import SimpleClassifier
from dataset import QuestionDataset
from feedback import save_feedback  # ✅ merkezi fonksiyonu import et

pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load dataset and model
DATASET_PATH = "questions.csv"
MODEL_PATH = "model.pth"
dataset = QuestionDataset(DATASET_PATH)
input_dim, output_dim = dataset.get_dims()
model = SimpleClassifier(input_dim, output_dim)
model.load_state_dict(torch.load(MODEL_PATH))
model.eval()

class PredictRequest(BaseModel):
    question: str

@app.post("/predict")
def predict(req: PredictRequest):
    x = dataset.vectorizer.transform([req.question]).toarray()
    x_tensor = torch.tensor(x[0], dtype=torch.float32)
    with torch.no_grad():
        output = model(x_tensor)
        pred = torch.argmax(output).item()
        topic = dataset.decode_label(pred)
    return {"topic": topic}

@app.post("/ocr")
def ocr(file: UploadFile = File(...)):
    image_bytes = file.file.read()
    image = Image.open(io.BytesIO(image_bytes))
    text = pytesseract.image_to_string(image, lang="tur")
    return {"text": text.strip()}

@app.post("/feedback")
def feedback(question: str = Form(...), topic: str = Form(...), is_correct: bool = Form(...)):
    save_feedback(question, topic, is_correct)  # ✅ artık burada çağrılıyor
    return {"status": "ok"}
