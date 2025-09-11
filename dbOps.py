import os
import sqlite3


def connectDB():
    os.makedirs('db',exist_ok=True)
    conn = sqlite3.connect('db/attendance.db')

    cursor = conn.cursor()

    cursor.execute("""
CREATE TABLE IF NOT EXISTS fingerprintLog (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   deviceId TEXT,
                   deviceLogId TEXT,
                   employeeId TEXT,
                   timestamp TEXT,
                    isSynced BOOLEAN DEFAULT 0,
                   UNIQUE(deviceId, timestamp, employeeId) )
""")
    
    conn.commit()
    conn.close()
    print('local database connected')


def saveData(data):
   try:
      conn = sqlite3.connect('db/attendance.db')
      cursor = conn.cursor()

      for log in data:
         cursor.execute("""
INSERT OR IGNORE INTO fingerprintLog (deviceId,deviceLogId,employeeId,timestamp) VALUES(?,?,?,?)
""",(log['deviceId'],log['deviceLogId'],log['employeeId'],log['timestamp'])) 
         
         conn.commit()
   except Exception as e:   
      print("Error saving data:", e)
   finally:
      conn.close()    
