from Service.hrisService import saveLogsToServer
from Repository.repository import connectDB, saveData
from Util.fingerPrintUtil import connectAllDevices,getAllAttendanceLogs
import time
import threading

def initialFetch(conn):
  logs = getAllAttendanceLogs(conn)
  saveData(logs)
  saveLogsToServer()

def hourlyFetch(conn):
   while True:
     time.sleep(60*1)    #to run on every 1 minute
     logs = getAllAttendanceLogs(conn)
     saveData(logs)
     saveLogsToServer()

def main():
    connectDB()
    conn = connectAllDevices()

    if(conn):
       initialFetch(conn)

       thread = threading.Thread(target=hourlyFetch, args=(conn,))
       thread.daemon = True
       thread.start()

       try:
        while True:
            time.sleep(1)
       except KeyboardInterrupt:
          print('Gracefully closing the program')
       except Exception as e:
          print('error occurred',e)
       finally:
           for device in conn:
               if hasattr(device, 'close'):  # Check if device has close method
                   device.close()
           print("Cleanup complete")   
       

if __name__ == "__main__":
    main()