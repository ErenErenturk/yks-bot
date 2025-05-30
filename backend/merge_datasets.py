import pandas as pd

# Orijinal ve geri bildirim verilerini oku
df_main = pd.read_csv("questions.csv")
df_mis = pd.read_csv("misclassified.csv")

# Boş/sahte soruları at (eğer varsa)
df_mis = df_mis[df_mis["question"] != "SORU_METNİ_EKLEMEN_LAZIM"]

# Birleştir
df_merged = pd.concat([df_main, df_mis], ignore_index=True)

# Karışık hale getir (isteğe bağlı)
df_merged = df_merged.sample(frac=1).reset_index(drop=True)

# Yeni eğitim seti olarak kaydet
df_merged.to_csv("questions_retrained.csv", index=False)
print("questions_retrained.csv dosyası oluşturuldu.")
