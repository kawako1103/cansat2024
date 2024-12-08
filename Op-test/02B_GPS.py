from ublox_gps import UbloxGps
import serial
import spidev
# Can also use SPI here - import spidev
# I2C is not supported

#port = serial.Serial('/dev/serial0', baudrate=38400, timeout=1)
port = spidev.SpiDev()
gps = UbloxGps(port)

def run():
  
  try: 
    print("Listenting for UBX Messages.")
    while True:
      try: 
        coords = gps.geo_coords()
        print(coords.lon, coords.lat)
      except (ValueError, IOError) as err:
        print(err)
  
  finally:
    port.close()

if __name__ == '__main__':
  run()
