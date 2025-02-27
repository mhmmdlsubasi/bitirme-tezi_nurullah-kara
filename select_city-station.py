import pandas as pd
from sklearn.metrics import r2_score


def calculate_r2(group):
    return r2_score(group["ORTALAMA_SICAKLIK_°C"], group["t2m_avg"])


ds = pd.read_csv("data/processed/merged_era5-mgm_station.csv")

ds["datetime"] = pd.to_datetime(ds["datetime"])

# Tüm veri için R² hesapla
r2_all = ds.groupby(["İl", "Istasyon_No"]).apply(calculate_r2)

r2_all = r2_all[r2_all >= 0.75]  # R² 0.75 den buyuk olan istasyonları al

ds = ds[ds["Istasyon_No"].isin(r2_all.index.get_level_values(1))]

ds.to_csv("data/processed/final.csv", index=False)
