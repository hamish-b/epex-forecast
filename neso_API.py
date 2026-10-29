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

def wait_for_forecast(resource_id, date_col, date_format, deadline="09:17"):

    target = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    deadline = datetime.strptime(deadline, "%H:%M").time()

    while datetime.now().time() < deadline:
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