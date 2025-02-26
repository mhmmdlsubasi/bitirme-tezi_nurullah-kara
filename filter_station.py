import pandas as pd

# Veriyi oku ve datetime sütununu tarih-zaman formatına çevir
df = pd.read_csv("data/processed/mgm.csv")
df["datetime"] = pd.to_datetime(df["datetime"])

# İlgili tarih aralığındaki verileri filtrele
baslangic_tarihi = "1994-01-01"
bitis_tarihi = "2024-12-01"
df_filtreli = df[
    (df["datetime"] >= baslangic_tarihi) & (df["datetime"] <= bitis_tarihi)
]

# Her istasyonun kaç farklı tarih verisine sahip olduğunu hesapla
istasyon_tarih_sayisi = df_filtreli.groupby("Istasyon_No")[
    "datetime"
].nunique()

# Benzersiz tarih sayılarının dağılımını büyükten küçüğe sırala ve ekrana yazdır
# print(sorted(istasyon_tarih_sayisi.unique(), reverse=True))

# Belirli bir eşik değerine göre istasyonları filtrele (örneğin 360 gün)
esik_gun_sayisi = 360
gecerli_istasyonlar = istasyon_tarih_sayisi[
    istasyon_tarih_sayisi >= esik_gun_sayisi
].index

# Filtrelenen istasyonları kullanarak nihai veri kümesini oluştur
df_sonuc = df_filtreli[df_filtreli["Istasyon_No"].isin(gecerli_istasyonlar)]

df_sonuc.to_csv("data/processed/mgm_filtered.csv", index=False)
