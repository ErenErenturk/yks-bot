# retrain.py
import pandas as pd

# Eksik/yanlış sınıflandırılan veriyi oku
feedback_df = pd.read_csv("feedback.csv")
misclassified = feedback_df[feedback_df["is_correct"] == False]

# misclassified.csv dosyasına kaydet
misclassified.to_csv("misclassified.csv", index=False)
print("misclassified.csv dosyası oluşturuldu.")

# Ana veri setini ve misclassified verisini birleştir
original_df = pd.read_csv("questions.csv")
retrained_df = pd.concat([original_df, misclassified], ignore_index=True)

# Yeni veri seti dosyası olarak kaydet
retrained_df.to_csv("questions_retrained.csv", index=False)
print("questions_retrained.csv dosyası oluşturuldu.")
