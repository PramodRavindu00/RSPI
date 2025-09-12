from devices import getAllDeviceConfigurations,saveLogsToServer
from dbOps import connectDB,saveData
import time
from zk import ZK
from logs import sample_data,sample_data_2,sample_data_3


def connectDevice(config):
    ip = config.get("ip")
    port = config.get("port")

    try:
            zk = ZK(ip,port)
            conn = zk.connect()
            return {
                "status": "connected",
                "connection": conn
            }
    except Exception as e:
        return {
            "status": "failed",
            "error": str(e)
        }

def connectAllDevices(retries = 5, delay=5):
  devices = getAllDeviceConfigurations()
  not_connected = devices.copy()
  connected = []
  attempt = 0

  while not_connected and attempt < retries : 
     failed_to_connect = []

     for device in not_connected:
        if connectDevice(device):
           print(f"{device['deviceName']} connected successfully")
           connected.append(device)
        else:
           failed_to_connect.append(device)

     if failed_to_connect:
        print(f"{len(failed_to_connect)} devices failed to connect. Retrying in {delay} seconds")
        time.sleep(delay)     

     not_connected = failed_to_connect
     attempt += 1


  if not_connected:
     print("Following devices could not be connected", [d['deviceName'] for d in not_connected])

  else: 
     print("All devices connected successfully!")   

  return connected


# def fetchLogsFromAllDevices(connected_devices):
#    all_logs = []
#    for device in connected_devices:
#       conn = device["connection"]
#       try: 
#          logs = conn.get_attendance()
#          for log in logs:
#             all_logs.append({
#                ""
#             })
#       except Exception as e:
            


#    return data

def main():
    connectDB()
    saveData(sample_data_3)
   #  latest_logs = getLatestLogs()
   #  print(latest_logs)
   #saveLogsToServer() 



if __name__ == "__main__":
    main()
    
    