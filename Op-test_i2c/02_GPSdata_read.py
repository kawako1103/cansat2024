import smbus
import time

# I2Cバスの番号（Raspberry Piの場合、通常1）
I2C_BUS = 1

# U-blox GPSモジュールのI2Cアドレス（例: 0x42）
GPS_ADDRESS = 0x42

# SMBusオブジェクトの作成
bus = smbus.SMBus(I2C_BUS)

data_gps = ""
printed = 0

def read_gps_data():
	try:
		gps_data = ''
		check_FF = 0
		invalid_period = 0
		while check_FF == 0:
			data_1chr = bus.read_i2c_block_data(GPS_ADDRESS, 0xFF, 8)
        
			for byte in data_1chr:
				if byte != 0xFF:
					#print(chr(byte))
					gps_data = gps_data.join(chr(byte))
					print(gps_data,end="")
					invalid_period = 0
				else:
					if invalid_period == 0:
						print("no data to send.")
						invalid_period = 1
						
						print("SEEEP")
						time.sleep(3)
					else:
						print("",end="")
						#check_FF = 1
		return gps_data

	except Exception as e:
		print(f"Error reading from GPS module: {e}")
		return None

while True:
	gps_value = read_gps_data()
	print("HI")

'''
	data_1chr = bus.read_i2c_block_data(GPS_ADDRESS, 0xFF, 1)
	if data_1chr[0] == 0xFF:
		if printed == 0:
			if data_gps != "":
				print(data_gps)
			data_gps = ""
			printed == 1
		else:
			print("-")
	else:
		#print(data_1chr[0])
		data_gps = data_gps.join(chr(data_1chr[0]))
'''
'''
    gps_value = read_gps_data()
    if gps_value is not None:
        #print(f"GPS value: {gps_value}")
        print(gps_value,end="")
    else:
        print("Failed to read GPS data")
    
    # 1秒ごとにデータを読み取る
    time.sleep(0.01)
'''
