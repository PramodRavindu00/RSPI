from hrisAPI import saveLogsToServer
from dbOps import connectDB, saveData
from fingerprintDevice import connectAllDevices,getAllAttendanceLogs
import time
import threading

def initialFetch(conn):
  logs = getAllAttendanceLogs(conn)
  saveData(logs)
  saveLogsToServer()

def hourlyFetch(conn):
   while True:
     time.sleep(60*60)    #to run on every 1 hour
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