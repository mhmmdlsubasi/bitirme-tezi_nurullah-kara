import os

import pandas as pd

dataset_folder = "data/raw/mevbis/"

# Klasördeki tüm TXT dosyalarını listele
csv_file = [
    file for file in os.listdir(dataset_folder) if file.endswith(".txt")
]

# Tüm TXT dosyalarını tek bir DataFrame'de birleştir
df_listesi = [
    pd.read_csv(os.path.join(dataset_folder, dosya), sep="|")
    for dosya in csv_file
]
birlesik_df = pd.concat(df_listesi, ignore_index=True)

column_rename = {
    "?stasyon Numaras?": "Istasyon_No",
    # "?stasyon Ad?": "Istasyon_Ad",
    "?l": "İl",
    # "?l?e": "İlçe",
    # "Rak?m": "Rakım",
}

birlesik_df = birlesik_df[
    ["?stasyon Numaras?", "?l", "Enlem", "Boylam"]
].rename(columns=column_rename)


rename_il = {
    "Adana": "Adana",
    "Antalya": "Antalya",
    "Hatay": "Hatay",
    "Burdur": "Burdur",
    "Isparta": "Isparta",
    "Kahramanmara?": "K. Maras",
    "Mersin": "Mersin",
    "Osmaniye ": "Osmaniye",
}

birlesik_df = birlesik_df.replace(rename_il)

birlesik_df.to_csv("data/processed/readme.csv", index=False)
