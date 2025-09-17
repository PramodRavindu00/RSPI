import requests
from Repository.repository import selectAllUnsyncedLogs,updateAllUnsyncedLogs
import os
from dotenv import load_dotenv

load_dotenv()

HRIS_BASE_URL = os.getenv("HRIS_BASE_URL")
BATCH_SIZE=100

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
        if not raw_data:
            print("No unsynced fingerprint logs")
            return

        for i in range(0,len(raw_data),BATCH_SIZE):
            batch = raw_data[i:i+BATCH_SIZE]
            data = [
            {
                "employeeCode": row[0],
                "deviceId":row[1],
                "timestamp": row[2],
                "clockType":row[3]
            }
            for row in batch
                    ]
            
            try:
                response = requests.post(url,json=data,timeout=10)
                response.raise_for_status()
                print(f"Batch {i//BATCH_SIZE + 1} ({len(data)} logs) synced successfully.")
                updateAllUnsyncedLogs(batch)
            except requests.exceptions.RequestException as e:
                print(f"Error sending batch {i//BATCH_SIZE + 1}: {e}")
                break 
    except requests.exceptions.RequestException as e:
       print(f"Error saving logs to the server: {e}")
       return None




