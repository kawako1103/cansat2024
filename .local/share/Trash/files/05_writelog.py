import smbus
import time
import pynmea2 

I2C_BUS = 1
GPS_ADDRESS = 0x42

# SMBusオブジェクトの作成
bus = smbus.SMBus(I2C_BUS)

# 緯度,経度,時間をlogファイルに上書きする
def write_log_gps(read_lon, read_lat):
    with open("gps_log.txt", "w") as f:
        #f.write(f"{read_lon},{read_lat},{time}\n")
        f.write(f"{read_lon},{read_lat}\n")


def proccess_data(data_nmea):
	#行でsplit
	data_nmea_arr = data_nmea.split("\r\n")
	#GPSが取得できない場合はこの値を返す
	read_lon = "-1"
	read_lat = "-1"

	for index_i in range(len(data_nmea_arr)):
		#print(data_nmea_arr[index_i], end=" ")
		start_index = data_nmea_arr[index_i].find('$') + 3
		end_index = data_nmea_arr[index_i].find(',')
		nmea_cat = data_nmea_arr[index_i][start_index : end_index]
		#print("nmea_cat:",nmea_cat,end="")
		if nmea_cat == 'RMC' or nmea_cat == 'GGA' or nmea_cat == 'GLL':
			try:
				#print("nmea_cat:",nmea_cat,end=", ")
				msg = pynmea2.parse(data_nmea_arr[index_i])
				#print("longitude:",msg.lon,", latitude:", msg.lat)
				read_lon = msg.lon
				read_lat = msg.lat
			except Exception as e:
				print("")
		#else:
			#print("<-not include lon,lat")
		if nmea_cat == 'GLL':
			try:
				print("nmea_cat:",nmea_cat,end=", ")
				msg = pynmea2.parse(data_nmea_arr[index_i])
				print("timestamp:",msg.timestamp)
				read_time = msg.timestamp
			except Exception as e:
				print("")
	return read_lon, read_lat

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

def get_lon_lat():
	rx_data_nmea = read_gps_data()
	read_lon, read_lat = proccess_data(rx_data_nmea)
	attempt = 0

	while read_lon == "-1" or read_lat == "-1" or attempt <= 6:
		print("GPS info not found(",attempt,") retrying...")
		attempt += 1
		rx_data_nmea = read_gps_data()
		read_lon, read_lat = proccess_data(rx_data_nmea)
		time.sleep(0.5)
		
	#print("read_lon:",read_lon,", read_lat:",read_lat)
	return read_lon, read_lat

while True:
	read_lon, read_lat = get_lon_lat()
	write_log_gps(read_lon, read_lat)
	print("Longitude:",read_lon,", Latitude:",read_lat)
	time.sleep(3)