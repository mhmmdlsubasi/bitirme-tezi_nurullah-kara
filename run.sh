#!/bin/bash

set -e  # Hata yakalama: Bir komut başarısız olursa betik durur.

# 1. MEVBİS'ten alınan HTML dosyalarını CSV'ye dönüştür.
mkdir -p data/processed/mevbis_csv-files
python3 ./mevbis_html-to-csv.py data/raw/mevbis/*.html
mv data/raw/mevbis/*.csv data/processed/mevbis_csv-files/

# 2. MGM ve açıklama dosyalarını birleştir.
python3 ./merge_benioku.py  # data/processed/readme.csv
python3 ./merge_mgm.py  # data/processed/mgm.csv

# 3. 1994-2024 yılları arasında en az 360 satır veriye sahip istasyonları filtrele.
python3 ./filter_station.py  # data/processed/mgm_filtered.csv

# 4. İstasyon konumlarına en yakın gridlere karşılık gelen değerleri filtrele ve kaydet.
python3 era5_station.py data/raw/t2m_monthly_avg.nc data/processed/akdeniz_station_mean.nc
python3 era5_station.py data/raw/t2m_daily_min.nc data/processed/akdeniz_station_min.nc
python3 era5_station.py data/raw/t2m_daily_max.nc data/processed/akdeniz_station_max.nc

# 5. ERA5 ve OMGİ verilerini tek bir tablo olarak birleştir.
python3 ./merge_era5-mgm_station.py  # data/processed/merged_era5-mgm_station.csv

# 6. Her il için R² değeri en yüksek olan istasyonu seç ve veri setini filtrele.
python3 ./select_city-station.py  # data/processed/final.csv

echo "Tüm işlemler başarıyla tamamlandı!"
