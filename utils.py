import pandas as pd


def build_demand_hours(demand: pd.DataFrame, format: str) -> pd.DataFrame:
    
    # converting datetimes and fixing midnight
    time_str = demand["CP_ST_TIME"].astype(str).str.zfill(4)
    time_str_end = demand["CP_END_TIME"].astype(str).str.zfill(4)

    midnight = time_str == "2400"
    midnight_end = time_str_end == "2400"
    time_str = time_str.mask(midnight, "0000")
    time_str_end = time_str_end.mask(midnight_end, "0000")

    # format needed since for some reason live and historical data are differently formatted
    
    date_str = pd.to_datetime(demand["TARGETDATE"], format = format).dt.strftime("%Y-%m-%d")

    demand["CP_ST_TIME"] = pd.to_datetime(
        date_str + " " + time_str.str[:2] + ":" + time_str.str[2:] + ":00"
    )
    demand["CP_END_TIME"] = pd.to_datetime(
        date_str + " " + time_str_end.str[:2] + ":" + time_str_end.str[2:] + ":00"
    )

    demand.loc[midnight, "CP_ST_TIME"] += pd.Timedelta(days=1)
    demand.loc[midnight_end, "CP_END_TIME"] += pd.Timedelta(days=1)

    demand = demand.drop(columns=["TARGETDATE"])

    # mapping each hour to its nearest period endpoint
    hours = pd.date_range(
        demand["CP_ST_TIME"].min().floor("h"),
        demand["CP_END_TIME"].max().ceil("h"),
        freq="h",
    )

    start = demand[["CP_ST_TIME", "FORECASTDEMAND"]].rename(columns={"CP_ST_TIME": "Endpoint"})
    end = demand[["CP_END_TIME", "FORECASTDEMAND"]].rename(columns={"CP_END_TIME": "Endpoint"})

    endpoints = (
        pd.concat([start, end], ignore_index=True)
        .sort_values("Endpoint")
        .reset_index(drop=True)
    )

    hourly_df = pd.DataFrame({"Hour": hours})
    hourly_df["Endpoint"] = hourly_df["Hour"]

    hourly_df = pd.merge_asof(
        hourly_df.sort_values("Hour"),
        endpoints,
        left_on="Hour",
        right_on="Endpoint",
        direction="nearest",
        allow_exact_matches=True,
    )

    # localise to UK
    demand_hours = hourly_df[["Hour", "FORECASTDEMAND"]].copy()
    demand_hours["Hour"] = demand_hours["Hour"].dt.tz_localize(
        "Europe/London", nonexistent="NaT", ambiguous="NaT"
    )

    return demand_hours