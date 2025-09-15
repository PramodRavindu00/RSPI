from hrisAPI import saveLogsToServer
from dbOps import connectDB, saveData
from fingerprintDevice import connectAllDevices,getAllAttendanceLogs

def main():
    connectDB()
    conn = connectAllDevices()
    logs = getAllAttendanceLogs(conn)
    saveData(logs)
    saveLogsToServer()


if __name__ == "__main__":
    main()