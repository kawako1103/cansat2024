import spidev

# SPIデバイスの設定
spi = spidev.SpiDev()
spi.open(0, 0)  # SPI0の0番目のデバイスを使用（Raspberry Piの場合）

# クロック周波数の設定
clock_freq_hz = 5500000  # 例: 1MHzの場合

spi.max_speed_hz = clock_freq_hz

try:
    while True:
        # SPIデータの送受信
        tx_data = [0x01, 0x02, 0x03]  # 送信するデータ（例）
        rx_data = spi.xfer2(tx_data)  # 送信して受信

        # 受信したデータをターミナルに出力
        print("Received data:", rx_data)

except KeyboardInterrupt:
    # Ctrl+Cが押されたら、SPIデバイスを閉じて終了する
    spi.close()
