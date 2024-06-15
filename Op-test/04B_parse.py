import spidev
import RPi.GPIO as GPIO
import pynmea2

def save_string_to_file(string, filename):
    with open(filename, 'a') as file:
        file.write(string)


# SPIデバイスの設定
spi = spidev.SpiDev()
spi.open(0, 0)  # SPI0の0番目のデバイスを使用（Raspberry Piの場合）

# クロック周波数の設定
spi.max_speed_hz = 1000000  # 例: 1MHzの場合

# Init
rx_data_nmea =''

try:
	count_FF = 0
	while True:

		tx_data = [0xFF]
		rx_data = spi.xfer(tx_data)
                
		if rx_data[0] == 0xFF:
			count_FF += 1
			if count_FF >= 50 and len(rx_data_nmea) >= 1:
				#spi.close()
				break
		else:
			count_FF = 0;
			print(".",end= "")
			rx_data_nmea += chr(rx_data[0])

	spi.close()
    
	print("\nReceived data:")
	print(rx_data_nmea)
	
	# 保存する文字列
	file_name = "log_rawstring.txt"
	save_string_to_file(rx_data_nmea, file_name)

	#split
	data_nmea_arr = rx_data_nmea.split("\r\n")
	print(data_nmea_arr)
	for index_i in range(len(data_nmea_arr)):
		msg = pynmea2.parse(data_nmea_arr[index_i])
		print(msg)

        


except KeyboardInterrupt:
	# Ctrl+Cが押されたら、SPIデバイスを閉じて終了する
	spi.close()
	print(rx_data_nmea)


