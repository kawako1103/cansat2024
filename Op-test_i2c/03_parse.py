import smbus
import time
import pynmea2 

I2C_BUS = 1
GPS_ADDRESS = 0x42

# SMBusオブジェクトの作成
bus = smbus.SMBus(I2C_BUS)

def proccess_data(data_nmea):
	#split
	data_nmea_arr = data_nmea.split("\r\n")
	#print("data_nmea_arr:",data_nmea_arr,"endof")
	for index_i in range(len(data_nmea_arr)):
		print(data_nmea_arr[index_i], end=" ")
		start_index = data_nmea_arr[index_i].find('$') + 3
		end_index = data_nmea_arr[index_i].find(',')
		nmea_cat = data_nmea_arr[index_i][start_index : end_index]
		#print("nmea_cat:",nmea_cat,end="")
		if nmea_cat == 'RMC' or nmea_cat == 'GGA' or nmea_cat == 'GLL':
			try:
				print("nmea_cat:",nmea_cat,end=", ")
				msg = pynmea2.parse(data_nmea_arr[index_i])
				print("longitude:",msg.lon,", latitude:", msg.lat)
			except Exception as e:
				print("")
		#else:
			#print("<-not include lon,lat")

def read_gps_data():
	try:
		rx_data_nmea = ''
		check = 0
		count_FF = 0
		while check == 0:
			rx_data = bus.read_i2c_block_data(GPS_ADDRESS, 0xFF, 16)
        
			for byte in rx_data:
				if byte != 0xFF:
					rx_data_nmea += chr(byte)
					count_FF = 0
				else:
					count_FF += 1
					#print(count_FF, len(rx_data_nmea))
					if count_FF >= 50  and len(rx_data_nmea) >= 1:
						#print("NoData Period")
						count_FF = 0
						check = 1
						
		return rx_data_nmea

	except Exception as e:
		print(f"Error reading from GPS module: {e}")
		return ""

while True:
	rx_data_nmea = read_gps_data()
	#print(rx_data_nmea)
	proccess_data(rx_data_nmea)
	print("SEEEP\n")
	time.sleep(1)
