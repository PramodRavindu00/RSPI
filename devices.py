import requests
from dbOps import selectAllUnsyncedLogs,updateAllUnsyncedLogs
import os
from dotenv import load_dotenv

load_dotenv()
HRIS_BASE_URL = os.getenv("HRIS_BASE_URL")

def getAllDeviceConfigurations():
    url = f"{HRIS_BASE_URL}/device-gateway/get-devices"

    try:
        response = requests.post(url,timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching device configurations: {e}")
        return None
        
def saveLogsToServer():
    url = f"{HRIS_BASE_URL}/attendance/saveFingerprintLogs"
    try:
        raw_data = selectAllUnsyncedLogs()
        if(len(raw_data)>0):
            data = [
                {
                    "employeeCode": row[0],
                    "deviceId":row[1],
                    "timestamp": row[2],
                    "clockType":row[3]
                }
                for row in raw_data
            ]
            response = requests.post(url,json=data,timeout=10)
            response.raise_for_status()
            updateAllUnsyncedLogs()
            return response.json()
        else:
            print('No unsynced fingerprint logs')
    except requests.exceptions.RequestException as e:
       print(f"Error saving logs to the server: {e}")
       return None




