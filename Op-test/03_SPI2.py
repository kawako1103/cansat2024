import spidev
import RPi.GPIO as GPIO

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
				break
		else:
			count_FF = 0;
			print(".",end= "")
			rx_data_nmea += chr(rx_data[0])

	spi.close()
	GPIO.cleanup()
    
	print("\nReceived data:")
	print(rx_data_nmea)

except KeyboardInterrupt:
	# Ctrl+Cが押されたら、SPIデバイスを閉じて終了する
	spi.close()
	GPIO.cleanup()
	print(rx_data_nmea)
