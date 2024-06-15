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
    while True:
        GPIO.output(CS_PIN, GPIO.HIGH)
        
        #rx_data = spi.readbytes(1)
        
        tx_data = [0xFF]
        rx_data = spi.xfer(tx_data)
        
        if rx_data[0] != 0xFF:
            #rx_data_str = chr(rx_data[0])
            #print(rx_data_str,end=" ")
            rx_data_nmea += chr(rx_data[0])
        
        if rx_data[0] == 0xFF and len(rx_data_nmea) >= 1:
            break
            
    GPIO.output(CS_PIN, GPIO.LOW)
    spi.close()
    GPIO.cleanup()
    
    print("Received data:",rx_data_nmea)

except KeyboardInterrupt:
    # Ctrl+Cが押されたら、SPIデバイスを閉じて終了する
    spi.close()
    GPIO.cleanup()
