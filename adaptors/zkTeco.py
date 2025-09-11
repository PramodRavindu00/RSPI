from zk import ZK, const

class ZKTecoPlugin:
    def init(self, ip='192.168.8.201', port=4370, timeout=5, password=0, force_udp=False):
        self.ip = ip
        self.port = port
        self.timeout = timeout
        self.password = password
        self.force_udp = force_udp
        self.conn = None

    def connect(self):
        zk = ZK(self.ip, port=self.port, timeout=self.timeout,
                password=self.password, force_udp=self.force_udp)
        
        try:
            self.conn = zk.connect()
            print(f"Connected to ZKTeco device at {self.ip}")
            
            # Play a test sound
            self.conn.test_voice()
            print("Test sound played on device")
            
            return True
        except Exception as e:
            print(f"Failed to connect to device: {e}")
            return False

    def get_attendance_logs(self):
        if not self.conn:
            print("Device not connected!")
            return []

        try:
            logs = self.conn.get_attendance()
            log_list = []
            for log in logs:
                log_list.append({
                    "user_id": log.user_id,
                    "timestamp": log.timestamp,
                    "status": log.status
                })
            print(f"Retrieved {len(log_list)} logs")
            return log_list
        except Exception as e:
            print(f"Failed to get logs: {e}")
            return []

    def disconnect(self):
        if self.conn:
            try:
                self.conn.disconnect()
                print("Disconnected from device")
            except Exception as e:
                print(f"Error during disconnect: {e}")
        else:
            print("Device was not connected")
