import smbus##
import time

# I2Cバスの番号（Raspberry Piの場合、通常1）
I2C_BUS = 1

# U-blox GPSモジュールのI2Cアドレス（例: 0x42）
GPS_ADDRESS = 0x42

# SMBusオブジェクトの作成
bus = smbus.SMBus(I2C_BUS)

#init Value
check_sum = 0
gps_value = ''

def read_gps_data():
	try:
        # U-blox GPSモジュールからデータを読み取る
		# 例: 8バイトのデータを読み取る場合
		data = bus.read_i2c_block_data(GPS_ADDRESS, 0xFD, 8)
        
		# 読み取ったデータを加工・処理（具体的なデータフォーマットに依存）
		# 例: NMEAフォーマットのデータを処理する
		#gps_data = ''.join(chr(byte) for byte in data)
		gps_data = ''
		for byte in data:
			if byte != 0xFF:
				print(gps_data)
			else:
				print("0xFF", end="")
				check_sum = 1
				break
		
		gps_data += chr(byte)
		return gps_data
		
	except Exception as e:
		print(f"Error reading from GPS module: {e}")
		return None

while check_sum == 0:
	gps_value = gps_value.join(read_gps_data())

print("gps_value = ")
print(gps_value)
    
