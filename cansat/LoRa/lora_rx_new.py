import serial
import time
import RPi.GPIO as GPIO
import csv

class LoRaTransmitter:
    def __init__(self, port, baudrate, reset_pin, log_file_path, data_file):
        self.ser = serial.Serial(port=port, baudrate=baudrate, timeout=None)
        self.reset_pin = reset_pin
        self.log_file_path = log_file_path
        self.data_file = data_file
        self._setup_gpio()

    def _setup_gpio(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.reset_pin, GPIO.OUT)

    def reset(self):
        GPIO.output(self.reset_pin, 1)
        time.sleep(0.3)
        GPIO.output(self.reset_pin, 0)
        time.sleep(2)

    def send_serial(self, msg: str):
        OK_check = False
        self.ser.write((msg + "\r\n").encode("ascii"))
        
        while not OK_check:
            data = self.ser.readline().rstrip()
            print(f"'{msg}' : {data}")
            
            if b"OK" in data:
                OK_check = True
                self.ser.reset_input_buffer()
                self.ser.reset_output_buffer()

    def read_latest_log_entry(self):
        try:
            with open(self.data_file, 'r') as file:
                reader = csv.reader(file)
                header = next(reader, None)  # ヘッダーをスキップ
                last_entry = None
                for row in reader:
                    last_entry = row  # 最後の行を取得
                
                if last_entry:
                    return {
                        "time_stamp": last_entry[0],
                        "gps_pos[0]": last_entry[1],
                        "gps_pos[1]": last_entry[2],
                        "azimuth": last_entry[3],
                        "deg": last_entry[4],
                        "distance": last_entry[5],
                        "velocity_value": last_entry[6],
                        "status": last_entry[7]
                    }
        except Exception as e:
            print(f"Error reading log file: {e}")
        return None

    def send_data(self, log_entry):
        if log_entry is not None:
            output = (
                f"4321FFFF,{log_entry['time_stamp']},{log_entry['gps_pos[0]']},{log_entry['gps_pos[1]']},"
                f"{log_entry['azimuth']},{log_entry['deg']},{log_entry['distance']},{log_entry['velocity_value']},"
                f"{log_entry['status']}\r\n"
            )
            
            with open(self.log_file_path, 'a') as log_file:
                self.ser.write(output.encode('ascii'))
                log_file.write(output)
                print(output.encode('ascii'))
            
            time.sleep(1)
        else:
            print("No valid data to send.")

    def initialize_device(self):
        self.reset()
        data = self.ser.readline().rstrip()
        print("rcv data : {0}".format(data))
        print(data)
        
        self.send_serial("2")
        self.send_serial("load")
        self.send_serial("bw 6")
        self.send_serial("panid 4321")
        self.send_serial("ownid FFFE")
        self.send_serial("ack 2")
        self.send_serial("rcvid 1")
        self.send_serial("transmode 2")
        self.send_serial("rssi 1")
        self.send_serial("sf 7")
        self.send_serial("save")
        self.send_serial("start")

    def run(self):
        while True:
            log_entry = self.read_latest_log_entry()
            self.send_data(log_entry)
            time.sleep(0.5)


def lora_tx_release_pre2():
    PORT = "/dev/ttyS0"
    BAUDRATE = 115200
    RESET_PIN = 25
    LOG_FILE_PATH = "/home/cansat-stu/cansat/sent_data_20240911.log"
    DATA_FILE = "/home/cansat-stu/cansat/test_log_mayu3.csv"

    lora_tx = LoRaTransmitter(PORT, BAUDRATE, RESET_PIN, LOG_FILE_PATH, DATA_FILE)
    lora_tx.initialize_device()
    lora_tx.run()


if __name__ == "__main__":
    lora_tx_release_pre2()