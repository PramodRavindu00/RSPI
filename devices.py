import requests

def getAllDeviceConfigurations():
    url = 'http://localhost:9061/device-gateway/get-devices'

    try:
        response = requests.post(url,timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print("Error fetching device configurations:{e}")
        return None

def saveLogsToServer(data):
    url = 'http://localhost:9061/attendance/save-fingerprint-logs'
    try:
        response = requests.post(url,json=data,timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(e)
        # print("Error saving logs to the server:{e}")
        return None




