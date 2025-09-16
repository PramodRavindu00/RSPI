from Service.hrisService import getAllDeviceConfigurations
import time
from datetime import timezone
from zk import ZK

def connectDevice(config):
    ip = config.get("ipAddress")
    port = config.get("port")

    try:
        zk = ZK(ip, port,timeout=5)
        conn = zk.connect()
        return conn
    except Exception as e:
        print(f"Error details: {e}") 
        return None


def connectAllDevices(retries=3, delay=3):
    devices_config = getAllDeviceConfigurations()
    if "data" not in devices_config or len(devices_config["data"]) == 0:
        return []
    
    all_devices = []
    for pi_device in devices_config["data"]:
        if "connectionDetails" in pi_device and len(pi_device["connectionDetails"]) > 0:
            for conn in pi_device["connectionDetails"]:
                all_devices.append(conn)

    not_connected = all_devices.copy()
    connected = []
    attempt = 0

    while not_connected and attempt < retries: 
        failed_to_connect = []

        for device in not_connected:
            conn = connectDevice(device)
            if conn:
                conn.test_voice()
                device_name = device.get('fingerPrintDevice', {}).get('name', 'Unknown Device')
                print(f"{device_name} connected successfully")
                
                connected.append({
                    "connection": conn,
                    "device": device
                })
            else:
                failed_to_connect.append(device)

        if failed_to_connect:
            print(f"{len(failed_to_connect)} device/s failed to connect. Retrying in {delay} seconds")
            time.sleep(delay)     

        not_connected = failed_to_connect
        attempt += 1

    if not_connected:
        failed_names = []
        for d in not_connected:
            name = d.get('fingerPrintDevice', {}).get('name', 'Unknown Device')
            failed_names.append(name)
        print("Following devices could not be connected:", failed_names)
    else: 
        print("All devices connected successfully!")   

    return connected


def getAllAttendanceLogs(connected_devices):
    all_logs = []
    for item in connected_devices:
        conn = item["connection"]     
        device = item["device"]       
        try:
            device_name = device.get('fingerPrintDevice', {}).get('name', 'Unknown Device')
            
            logs = conn.get_attendance()
            if logs:
                for log in logs:
                    log_data = {
                        "employeeCode": log.user_id,
                        "timestamp": log.timestamp.replace(tzinfo=timezone.utc).isoformat(),
                        "deviceLogId": log.uid,
                        "deviceId": device.get("fingerPrintDeviceId", "Unknown"),
                    }
                    all_logs.append(log_data)
                print(f"Fetched {len(logs)} logs from {device_name}")
            else:
                print(f"No logs found for {device_name}")
        except Exception as e:
            device_name = device.get('fingerPrintDevice', {}).get('name', 'Unknown Device')
            print(f"Error fetching logs from {device_name}: {e}")
    return all_logs

