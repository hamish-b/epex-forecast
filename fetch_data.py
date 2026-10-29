import requests, time
import pandas as pd
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


API = "https://api.neso.energy/api/3/action/datastore_search_sql"


import time
import requests
import pandas as pd
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

API = "https://api.neso.energy/api/3/action/datastore_search"
WIND_ID = "b2f03146-f05d-4824-a663-3a4f36090c71"
DEMAND_ID = "aec5601a-7f3e-4c4c-bf56-d8e4184d3c5b"

def wait_for_forecast(resource_id, date_col, date_format, deadline="2026-10-30 09:17"):

    target = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    deadline = datetime.strptime(deadline, "%Y-%m-%d %H:%M")

    while datetime.now() < deadline:
        r = requests.get(
            "https://api.neso.energy/api/3/action/datastore_search",
            params={"resource_id": resource_id, "limit": 1000},
        )
        df = pd.DataFrame(r.json()["result"]["records"])
        dates = pd.to_datetime(df[date_col], format=date_format, errors="coerce")
        day = df[dates.dt.strftime("%Y-%m-%d") == target]

        if not day.empty:
            return day

        time.sleep(35)

    raise TimeoutError(f"No forecast available for {target}")

def fetch_forecasts(deadline="2026-10-30 09:17"):

    wind = wait_for_forecast(
        WIND_ID,
        date_col="Date",
        date_format="%Y-%m-%d",
        deadline=deadline
    )

    demand = wait_for_forecast(
        DEMAND_ID,
        date_col="TARGETDATE",
        date_format="%Y%m%d",
        deadline=deadline
    )

    return wind, demand