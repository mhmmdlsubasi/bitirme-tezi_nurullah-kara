import pandas as pd
import xarray as xr

mgm = pd.read_csv("data/processed/mgm_filtered.csv")
era5_min = xr.open_dataset("data/processed/akdeniz_station_min.nc")
era5_mean = xr.open_dataset("data/processed/akdeniz_station_mean.nc")
era5_max = xr.open_dataset("data/processed/akdeniz_station_max.nc")

# mgm.rename(columns={"Istasyon_No": "station"}, inplace=True)
mgm = mgm[
    ["Istasyon_No", "İl", "Istasyon_Adi", "datetime", "ORTALAMA_SICAKLIK_°C"]
]
# ERA5 -----------------------------------------------------------------------
era5_min = era5_min.to_dataframe().reset_index()
era5_mean = era5_mean.to_dataframe().reset_index()
era5_max = era5_max.to_dataframe().reset_index()

# Her yılın aylık ortalamalarına dönüştürülmesi
era5_min["time"] = era5_min["time"].dt.to_period("M")
era5_min = era5_min.groupby(["istno", "time"]).mean().reset_index()
era5_min["time"] = era5_min["time"].dt.to_timestamp()

era5_max["time"] = era5_max["time"].dt.to_period("M")
era5_max = era5_max.groupby(["istno", "time"]).mean().reset_index()
era5_max["time"] = era5_max["time"].dt.to_timestamp()

# NaN veri döndüren istasyonların filtrelenmesi
nan_stations = list(era5_mean[era5_mean["t2m"].isna()]["istno"].unique())
mgm = mgm[~mgm["Istasyon_No"].isin(nan_stations)]


rename_column = {"istno": "Istasyon_No", "time": "datetime"}
era5_min = era5_min.rename(columns=rename_column)
era5_mean = era5_mean.rename(columns=rename_column)
era5_max = era5_max.rename(columns=rename_column)

era5_min = era5_min.rename(columns={"t2m": "t2m_min"})
era5_mean = era5_mean.rename(columns={"t2m": "t2m_avg"})
era5_max = era5_max.rename(columns={"t2m": "t2m_max"})

mgm["datetime"] = pd.to_datetime(mgm["datetime"])  # Object → Datetime
era5_mean["datetime"] = pd.to_datetime(era5_mean["datetime"])


merged_df = (
    mgm.merge(era5_min, on=["Istasyon_No", "datetime"], how="inner")
    .merge(era5_mean, on=["Istasyon_No", "datetime"], how="inner")
    .merge(era5_max, on=["Istasyon_No", "datetime"], how="inner")
)

merged_df.to_csv("data/processed/merged_era5-mgm_station.csv", index=False)
