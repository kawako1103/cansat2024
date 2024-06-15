import smbus
import time

I2C_BUS = 1
GPS_ADDRESS = 0x42

# SMBusオブジェクトの作成
bus = smbus.SMBus(I2C_BUS)

def read_gps_data():
	try:
		rx_data_nmea = ''
		check = 0
		count_FF = 0
		while check == 0:
			rx_data = bus.read_i2c_block_data(GPS_ADDRESS, 0xFF, 1)
        
			for byte in rx_data:
				if byte != 0xFF:
					rx_data_nmea += chr(byte)
					print(rx_data_nmea,end="")
					count_FF = 0
				else:
					count_FF += 1
					#print(count_FF, len(rx_data_nmea))
					if count_FF >= 50  and len(rx_data_nmea) >= 1:
						print("No Data Period")
						count_FF = 0
						check = 1
						
						
		return rx_data_nmea

	except Exception as e:
		print(f"Error reading from GPS module: {e}")
		return None

while True:
	rx_data_nmea = read_gps_data()
	print("\nSEEEP\n")
	time.sleep(5)
