import pandas as pd

# CSV'den oku
df = pd.read_csv("feedback.csv")

# Sadece yanlış tahmin edilenler
wrong_preds = df[df["is_correct"] == False]

# Eğer orijinal sorular da tutulmuş olsaydı burada eşleştirilirdi.
# Ama şu anlık elimizde sadece 'topic' var, bu yüzden placeholder örnekler koyacağız.
# Gerçek kullanımda soru metniyle eşlenmelidir.

# Sahte örnek metinler yerleştirelim (manuel veri düzeltme için)
wrong_preds["question"] = "SORU_METNİ_EKLEMEN_LAZIM"

# Kolon sıralamasını düzelt
wrong_preds = wrong_preds[["question", "topic"]]

# Yeni CSV dosyası olarak kaydet
wrong_preds.to_csv("misclassified.csv", index=False)
print("misclassified.csv dosyası oluşturuldu.")
