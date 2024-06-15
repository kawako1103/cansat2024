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
clock_freq_hz = 1000000  # 例: 1MHzの場合

spi.max_speed_hz = clock_freq_hz

# CS_N
CS_PIN = 8

GPIO.setmode(GPIO.BOARD)
GPIO.setup(CS_PIN, GPIO.OUT) 
GPIO.output(CS_PIN, GPIO.LOW)

# Init
rx_data_nmea =''

try:
	count_FF = 0
	while True:
		GPIO.output(CS_PIN, GPIO.HIGH)

		tx_data = [0xFF]
		rx_data = spi.xfer(tx_data)
                
		if rx_data[0] == 0xFF:
			count_FF += 1
			if count_FF >= 50 and len(rx_data_nmea) >= 1:
				spi.close()
				GPIO.cleanup()
				break
		else:
			count_FF = 0;
			print(".",end= "")
			rx_data_nmea += chr(rx_data[0])

	GPIO.output(CS_PIN, GPIO.LOW)

    
	print("\nReceived data:")
	print(rx_data_nmea)
	
	# 保存する文字列
	file_name = "log_rawstring.txt"
	save_string_to_file(rx_data_nmea, file_name)

	#split
	data_nmea_arr = rx_data_nmea.split("\r\n")
	print(data_nmea_arr)
	for index_i in range(len(data_nmea_arr)):
		
		try:
			msg = pynmea2.parse(data_nmea_arr[index_i])
			print(repr(msg))
			#print(msg)
			print("lat:",end='')
			print(msg.lat)
			print("lon:",end='')
			print(msg.lon)
			print("")
		except pynmea2.ParseError as e:
			#print('Parse error: {}'.format(e))
			continue
        


except KeyboardInterrupt:
	# Ctrl+Cが押されたら、SPIデバイスを閉じて終了する
	spi.close()
	GPIO.cleanup()
	print(rx_data_nmea)


