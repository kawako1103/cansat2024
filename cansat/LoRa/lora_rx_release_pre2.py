import serial
import time
import RPi.GPIO as GPIO

class LoRaReceiver:
    """
    A class to handle the reception of data via LoRa using UART communication with a Raspberry Pi.
    """

    def __init__(self, port, baudrate, reset_pin, log_file_path):
        """
        Initialize the LoRaReceiver with the specified UART port, baudrate, reset pin, and log file path.
        """
        self.ser = serial.Serial(port=port, baudrate=baudrate, timeout=None)
        self.reset_pin = reset_pin
        self.log_file_path = log_file_path
        self._setup_gpio()

    def _setup_gpio(self):
        """
        Set up the GPIO pin for resetting the LoRa module.
        """
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.reset_pin, GPIO.OUT)

    def reset(self):
        """
        Reset the LoRa module using the GPIO pin.
        """
        GPIO.output(self.reset_pin, 1)
        time.sleep(0.3)
        GPIO.output(self.reset_pin, 0)
        time.sleep(2)

    def send_serial(self, msg: str):
        """
        Send a command to the LoRa module via UART and wait for an "OK" response.
        """
        OK_check = False
        self.ser.write((msg + "\r\n").encode("ascii"))
        
        while not OK_check:
            data = self.ser.readline().rstrip()
            print(f"'{msg}' : {data}")
            
            if b"OK" in data:
                OK_check = True
                self.ser.reset_input_buffer()
                self.ser.reset_output_buffer()

    def decoder(self):
        """
        Decode incoming data from the LoRa module, print the relevant information,
        and save it to a log file.
        """
        with open(self.log_file_path, 'a') as log_file:
            while self.ser.in_waiting > 0:
                data = self.ser.readline().rstrip().decode()
                if data != '':
                    RSSI_hex, PAN, ID, LAT, LON = data[0:4], data[4:8], data[8:12], data[12:23], data[24:34]
                    formatted_data = f"{self.hex2dec(RSSI_hex, 16)}dBm,{PAN},{ID},{LAT},{LON}"
                    log_file.write(formatted_data + '\n')
                    if LAT == "00000.00000" and LON == "00000.00000":
                        print(f"Failed to obtain latitude and longitude from GPS (RSSI:{self.hex2dec(RSSI_hex, 16)}dBm, PANID:{PAN}, ID:{ID})")
                    else:
                        print(formatted_data)

    def hex2dec(self, x: str, bit: int) -> str:
        """
        Convert a hexadecimal string to a decimal value, considering the specified bit size.
        """
        dec = int(x, 16)
        if dec >> bit:
            raise ValueError
        return dec - (dec >> (bit - 1) << bit)

    def initialize_device(self):
        """
        Initialize the LoRa module by resetting it and sending the necessary setup commands.
        """
        self.reset()
        data = self.ser.readline().rstrip()
        print("rcv data : {0}".format(data))
        
        self.send_serial("2")
        self.send_serial("load")
        self.send_serial("bw 6")
        self.send_serial("panid 4321")
        self.send_serial("ownid FFFD")
        self.send_serial("ack 2")
        self.send_serial("rcvid 1")
        self.send_serial("transmode 2")
        self.send_serial("rssi 1")
        self.send_serial("sf 7")
        self.send_serial("save")
        self.send_serial("start")

    def run(self):
        """
        Continuously decode and process incoming data from the LoRa module.
        """
        while True:
            self.decoder()


if __name__ == "__main__":
    # Parameters for the LoRa receiver
    PORT = "/dev/ttyS0"
    BAUDRATE = 115200
    RESET_PIN = 12
    LOG_FILE_PATH = "/home/busan-rx/oldest-rx/received_data_log.txt"  # Path for saving received data

    # Create a LoRaReceiver object and initialize it
    lora_rx = LoRaReceiver(PORT, BAUDRATE, RESET_PIN, LOG_FILE_PATH)
    lora_rx.initialize_device()

    # Start the main loop
    lora_rx.run()
