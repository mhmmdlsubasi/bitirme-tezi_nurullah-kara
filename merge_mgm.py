import os

import pandas as pd

dataset_folder = "data/processed/mevbis_csv-files/"

# Klasördeki tüm CSV dosyalarını listele
csv_file = [
    file for file in os.listdir(dataset_folder) if file.endswith(".csv")
]

# Tüm CSV dosyalarını tek bir DataFrame'de birleştir
dfs = [pd.read_csv(os.path.join(dataset_folder, dosya)) for dosya in csv_file]

data_df = pd.concat(dfs, ignore_index=True)
location_df = pd.read_csv("data/processed/readme.csv")
remove_df = pd.read_csv("stations_to_delete.csv")

rename_istasyonAdi = {
    "AKSU/BOZTEPE": "AKSU/BOZTEPE TİGEM",
    "ANTALYA": "ANTALYA BÖLGE",
    "DULKADİROĞLU": "DULKADİROĞLU/ELMALAR ORMAN SAHASI",
    "HATAY": "HATAY HAVALİMANI",
    "HATAY TARIM": "HATAY TARIM ISL",
    "ISPARTA/GÖNE": "ISPARTA/GÖNEN",
    "KAHRAMANMAR": "KAHRAMANMARAŞ",
    "KEMER": "KEMER ANTALYA",
    "MERSİN/AYDINC": "MERSİN/AYDINCIK",
    "Mezitli/Çevlik": "Mezitli/Çevlik Köyü",
    "ONİKİŞUBAT/TE": "ONİKİŞUBAT/TEKİR BELDESİ",
    "TOROSLAR/ARS": "TOROSLAR/ARSLANKÖY",
    "YENİŞARBADEM": "YENİŞARBADEMLİ",
    "YÜREĞİR/ÇUKU": "YÜREĞİR/ÇUKUROVA TARIM ARŞ. (TAGEM)",
    "ÇAĞLAYANCERİ": "ÇAĞLAYANCERİT",
}
data_df = data_df.replace(rename_istasyonAdi)


data_df = data_df[~data_df["Istasyon_No"].isin(remove_df["Istasyon_No"])]
data_df = data_df[data_df["AY"] != 13]
data_df["Istasyon_Adi"] = data_df["Istasyon_Adi"].str.capitalize()

something_rename = {
    "K. Maras": "Kahramanmaraş",
    "Afşi̇n": "Afşin",
    "Osmani̇ye": "Merkez",
    "Korkuteli̇": "Korkuteli",
    "Tefenni̇": "Tefenni",
}
data_df["Istasyon_Adi"] = data_df["Istasyon_Adi"].replace(something_rename)
data_df["Istasyon_Adi"] = data_df["Istasyon_Adi"].str.capitalize()

data_df = pd.merge(data_df, location_df, on="Istasyon_No", how="inner")
data_df["datetime"] = pd.to_datetime(
    data_df["YIL"].astype(str) + "-" + data_df["AY"].astype(str) + "-01"
)

data_df.to_csv("data/processed/mgm.csv", index=False)
