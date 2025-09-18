from datetime import datetime
import requests
import pytz

ip_info_response = requests.get("https://ipinfo.io/json")
tz_name = ip_info_response.json().get("timezone")

def localizeTimestamp(timestamp):
    tz_obj = pytz.timezone(tz_name)
    if isinstance(timestamp, str):
        dt = datetime.fromisoformat(timestamp)
    else:
        dt = timestamp
    if dt.tzinfo is None:
        dt = tz_obj.localize(dt)

    return dt.isoformat()
