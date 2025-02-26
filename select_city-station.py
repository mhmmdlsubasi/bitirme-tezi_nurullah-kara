import pandas as pd
from sklearn.metrics import r2_score


def calculate_r2(group):
    return r2_score(group["ORTALAMA_SICAKLIK_°C"], group["t2m_avg"])


ds = pd.read_csv("data/processed/merged_era5-mgm_station.csv")

ds["datetime"] = pd.to_datetime(ds["datetime"])

# Tüm veri için R² hesapla
r2_all = ds.groupby(["İl", "Istasyon_No"]).apply(calculate_r2)

# Her ilin maksimum R² değerine sahip istasyonunu seç
max_r2_istasyonlari = r2_all.groupby("İl").idxmax()

# Seçilen istasyonların R² değerlerini ve bilgilerini al
max_r2_istasyonlari = r2_all.loc[max_r2_istasyonlari]

# print(max_r2_istasyonlari)

ds = ds[ds["Istasyon_No"].isin(max_r2_istasyonlari.index.get_level_values(1))]

selected_stations = list(ds["Istasyon_No"].unique())

ds = ds[ds["Istasyon_No"].isin(selected_stations)]

ds.to_csv("data/processed/final.csv", index=False)
