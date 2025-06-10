import serial
import csv
import time

REPEAT_TIMEOUT = 15  # saniye
recent_smells = {}

class KokuDedektor:
    def __init__(self, port, baudrate, filename):
        self.port = port
        self.baudrate = baudrate
        self.filename = filename
        self.ser = None
        self.writer = None
        self.file = None
        self.running = False
        self.callback = None

    def start(self):
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=1)
            time.sleep(2)
            self.running = True
            self.file = open(self.filename, 'w', newline='', encoding='utf-8')
            self.writer = csv.writer(self.file)
            self.writer.writerow(["Zaman(ms)", "MQ135 Değeri", "Koku"])
        except Exception as e:
            raise e

    def stop(self):
        self.running = False
        if self.ser:
            self.ser.close()
        if self.file:
            self.file.close()

    def read_line(self):
        if not self.running:
            return None
        try:
            line = self.ser.readline().decode('utf-8').strip()
            if line:
                parts = line.split(',')
                if len(parts) == 3:
                    return parts  # [time_ms, value, smell]
        except:
            return None
        return None

    def handle_manual_smell(self, smell):
        now_ms = int(time.time() * 1000)
        return [now_ms, 0, smell]

    def should_skip_smell(self, smell):
        now = time.time()
        last_time = recent_smells.get(smell)
        if last_time and (now - last_time) < REPEAT_TIMEOUT:
            return True
        recent_smells[smell] = now
        return False

    def log_smell(self, time_ms, value, smell):
        if self.writer:
            self.writer.writerow([time_ms, value, smell])
