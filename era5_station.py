import argparse
import os

import pandas as pd
import xarray as xr


def process_data(era5_path, output_path):
    # Sabit MGM dosya yolu
    mgm_path = "data/processed/mgm_filtered.csv"

    # ERA5 ve MGM verilerini oku
    mgm = pd.read_csv(mgm_path)  # İstasyon bilgileri
    era5 = xr.open_dataset(era5_path)  # ERA5 sıcaklık verileri

    # Akdeniz bölgesinin genel sınırlarını belirle
    era5 = era5.sel(latitude=slice(45, 30), longitude=slice(20, 50))

    # Kelvin → °C dönüşümü
    era5["t2m"] -= 273.15

    # Her istasyon için sıcaklık değerlerini saklayacak listeler
    istno_list = []
    values = []

    mgm_grouped = mgm.groupby("Istasyon_No", as_index=False)[
        ["Enlem", "Boylam"]
    ].mean()

    # MGM verisindeki her istasyon için en yakın grid noktasını bul
    for istno, lat, lon in mgm_grouped[
        ["Istasyon_No", "Enlem", "Boylam"]
    ].values:
        station = era5.sel(latitude=lat, longitude=lon, method="nearest")
        values.append(station["t2m"])  # DataArray olarak saklanıyor
        istno_list.append(istno)  # İstasyon numarasını ekle

    # DataArray'leri tek bir DataSet içinde birleştir
    ds_final = xr.Dataset(
        data_vars={
            "t2m": (["istno", "time"], xr.concat(values, dim="istno").values),
        },
        coords={
            "istno": istno_list,
            "time": era5.valid_time.values,  # Zaman değişkeni
        },
    )

    # Çıktı dosyasını kaydet
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    ds_final.to_netcdf(output_path)

    print(f"İşlem tamamlandı! NetCDF dosyası kaydedildi: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="ERA5 verilerini işler ve sabit MGM verisi ile eşleştirir."
    )
    parser.add_argument("era5_path", type=str, help="ERA5 NetCDF dosya yolu")
    parser.add_argument(
        "output_path", type=str, help="Çıktı NetCDF dosya yolu"
    )
    args = parser.parse_args()

    process_data(args.era5_path, args.output_path)
