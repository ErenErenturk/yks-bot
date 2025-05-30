// frontend/src/api.js
import axios from "axios";

const API_URL = "http://localhost:8000"; // FastAPI backend URL

export async function predictTopic(question) {
  try {
    const res = await axios.post(`${API_URL}/predict`, { question });
    return res.data;
  } catch (err) {
    console.error("Tahmin hatası:", err);
    return { error: "Tahmin yapılamadı" };
  }
}

export async function extractText(file) {
  try {
    const formData = new FormData();
    formData.append("file", file);
    const res = await axios.post(`${API_URL}/ocr`, formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    return res.data;
  } catch (err) {
    console.error("OCR hatası:", err);
    return { error: "Görselden metin okunamadı" };
  }
}

export async function sendFeedback({ question, topic, is_correct }) {
  try {
    const formData = new FormData();
    formData.append("question", question);
    formData.append("topic", topic);
    formData.append("is_correct", is_correct);

    const res = await axios.post(`${API_URL}/feedback`, formData);
    return res.data;
  } catch (err) {
    console.error("Geri bildirim hatası:", err);
    return { error: "Geri bildirim gönderilemedi" };
  }
}
