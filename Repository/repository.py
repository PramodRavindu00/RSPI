import os
import sqlite3
from datetime import datetime

def connectDB():
   os.makedirs('db',exist_ok=True)
   conn = sqlite3.connect('db/attendance.db')

   cursor = conn.cursor()

   cursor.execute("""
   CREATE TABLE IF NOT EXISTS fingerprintLog (
   deviceId TEXT,
   deviceLogId TEXT,
   employeeCode TEXT,
   timestamp TEXT,
   clockType TEXT,               
   isSynced BOOLEAN DEFAULT 0,
   PRIMARY KEY (deviceId, timestamp, employeeCode)
   )
   """)
   conn.commit()
   conn.close()
   print('local database connected')


def saveData(data):
   if len(data) > 0:
      try:
         conn = sqlite3.connect('db/attendance.db')
         cursor = conn.cursor()

         for log in data:
            log_date = datetime.fromisoformat(log['timestamp']).date()
            #check the employee has existing record with the same date to determine in or out
            cursor.execute("""
            SELECT COUNT(*) FROM fingerprintLog WHERE employeeCode = ? AND DATE(timestamp)= ? """,(log['employeeCode'],log_date))
            existing_count = cursor.fetchone()[0]

            if existing_count ==0:   #no record found its the clock In
               clock_type = "In"
            elif existing_count == 1:   #1 record found its the clock Out
               clock_type = "Out"
            else :                #all other punches will be ignored
               continue

            cursor.execute("""
            INSERT OR IGNORE INTO fingerprintLog (deviceId,deviceLogId,employeeCode,timestamp,clockType) VALUES(?,?,?,?,?)
            """,(log['deviceId'],log['deviceLogId'],log['employeeCode'],log['timestamp'],clock_type)) 
            conn.commit()
      except Exception as e:   
         print("Error saving data:", e)
      finally:
         conn.close()

def selectAllUnsyncedLogs():
      try:
         conn = sqlite3.connect('db/attendance.db')
         cursor = conn.cursor()
         cursor.execute("""
         SELECT employeeCode,deviceId,timestamp,clockType FROM fingerprintLog WHERE isSynced = 0""")
         rows = cursor.fetchall()
         return rows
      except Exception as e:
        print("Error retrieving Unsynced logs:", e)
      finally:
         conn.close()

def updateAllUnsyncedLogs(batch):
    try:
        conn = sqlite3.connect('db/attendance.db')
        cursor = conn.cursor()
        for row in batch:
         employeeCode,deviceId,timestamp,clockType = row[0],row[1],row[2],row[3]
         cursor.execute("""
         UPDATE fingerprintLog
         SET isSynced = 1
            WHERE employeeCode = ? AND deviceId = ? AND timestamp = ? AND clockType = ? AND isSynced = 0
            """, (employeeCode, deviceId, timestamp, clockType))
         conn.commit()  
        print(f"{cursor.rowcount} row/s updated as synced.")
    except Exception as e:
        print(f"Error updating Unsynced logs: {e}")
    finally:
        conn.close()



