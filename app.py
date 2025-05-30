# app.py
import streamlit as st
from model import SimpleClassifier
from dataset import QuestionDataset
import torch
from collections import Counter
import csv
import os

def save_feedback_to_csv(question, topic, is_correct):
    file_exists = os.path.isfile("feedback.csv")
    with open("feedback.csv", mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["question", "topic", "is_correct"])
        writer.writerow([question, topic, is_correct])

# Başlık
st.title("YKS Soru Konu Tahmini")
st.write("Bir soru girin, sistem hangi konuya ait olduğunu tahmin etsin.")

# Dataset ve model
dataset = QuestionDataset("questions.csv")
input_dim, output_dim = dataset.get_dims()
model = SimpleClassifier(input_dim, output_dim)
model.load_state_dict(torch.load("model.pth"))
model.eval()

# Kullanıcı geçmişi (oturum bazlı)
if "history" not in st.session_state:
    st.session_state.history = []
if "feedback" not in st.session_state:
    st.session_state.feedback = []  # (tahmin edilen konu, doğru mu?)
if "last_topic" not in st.session_state:
    st.session_state.last_topic = None
if "awaiting_feedback" not in st.session_state:
    st.session_state.awaiting_feedback = False

# Kullanıcıdan giriş
user_input = st.text_area("Soru", "")

if st.button("Tahmin Et") and user_input.strip() != "":
    x = dataset.vectorizer.transform([user_input]).toarray()
    x_tensor = torch.tensor(x[0], dtype=torch.float32)
    with torch.no_grad():
        output = model(x_tensor)
        pred = torch.argmax(output).item()
        topic = dataset.decode_label(pred)
        st.success(f"Tahmin Edilen Konu: **{topic}**")

        # Kullanıcının tahmin geçmişine ekle
        st.session_state.history.append(topic)
                # Tahmini son kayıta al
        st.session_state.last_topic = topic
        st.session_state.awaiting_feedback = True

# İstatistik göster
if st.session_state.history:
    st.subheader("📊 Konu İstatistiklerin")
    counts = Counter(st.session_state.history)
    total = sum(counts.values())
    for topic, count in counts.items():
        st.write(f"- {topic}: {count} soru (%{100 * count / total:.1f})")

# Kaynak öneri tabanı
recommendations = {
    "paragraf": ["Paragrafik kanalından her gün 10 soru", "Palme Paragraf Soru Bankası"],
    "problemler": ["Tonguç Problem Kampı", "3-4-5 TYT Matematik"],
    "dilbilgisi": ["Eksen Yayınları Konu Anlatımı", "Hocalara Geldik - Dilbilgisi Serisi"]
}

# Eksik ve yoğun alanlar
if st.session_state.history:
    counts = Counter(st.session_state.history)
    if len(counts) >= 2:
        most_common = counts.most_common()
        en_fazla = most_common[0][0]
        en_az = most_common[-1][0]

        st.markdown("---")
        st.subheader("🎯 Kişiselleştirilmiş Öneriler")

        st.markdown(f"🔹 En çok çalıştığın konu: **{en_fazla}**")
        if en_fazla in recommendations:
            st.write("Bu konuda kendini geliştirmeye devam etmek için öneriler:")
            for rec in recommendations[en_fazla]:
                st.write(f"- {rec}")

        st.markdown(f"🔸 Geri planda kalan konu: **{en_az}**")
        if en_az in recommendations:
            st.write("Bu konuyu biraz daha öne alman faydalı olabilir:")
            for rec in recommendations[en_az]:
                st.write(f"- {rec}")

# Kullanıcı geri bildirimi (Doğru mu?)
if st.session_state.awaiting_feedback:
    st.subheader("🧠 Bu tahmin doğru muydu?")
    col1, col2 = st.columns(2)

    if col1.button("✅ Evet"):
        save_feedback_to_csv(user_input, st.session_state.last_topic, True)
        st.session_state.feedback.append((st.session_state.last_topic, True))
        st.session_state.awaiting_feedback = False
        st.success("Teşekkürler, doğru olarak kaydedildi.")

    if col2.button("❌ Hayır"):
        save_feedback_to_csv(user_input, st.session_state.last_topic, False)
        st.session_state.feedback.append((st.session_state.last_topic, False))
        st.session_state.awaiting_feedback = False
        st.info("Geri bildirimin için teşekkürler, yanlış olarak kaydedildi.")
