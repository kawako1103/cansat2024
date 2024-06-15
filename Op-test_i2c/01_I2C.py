import smbus
import time

# I2Cバスの番号（Raspberry Piの場合、通常1）
I2C_BUS = 1

# U-blox GPSモジュールのI2Cアドレス（例: 0x42）
GPS_ADDRESS = 0x42

# SMBusオブジェクトの作成
bus = smbus.SMBus(I2C_BUS)

def read_gps_data():
    try:
        # U-blox GPSモジュールからデータを読み取る
        # 例: 8バイトのデータを読み取る場合
        data = bus.read_i2c_block_data(GPS_ADDRESS, 0xFF, 8)
        
        # 読み取ったデータを加工・処理（具体的なデータフォーマットに依存）
        # 例: NMEAフォーマットのデータを処理する
        gps_data = ''.join(chr(byte) for byte in data)
        
        return gps_data
    except Exception as e:
        print(f"Error reading from GPS module: {e}")
        return None

while True:
    gps_value = read_gps_data()
    if gps_value is not None:
        #print(f"GPS value: {gps_value}")
        print(gps_value,end="")
    else:
        print("Failed to read GPS data")
    
    # 1秒ごとにデータを読み取る
    time.sleep(0.01)
