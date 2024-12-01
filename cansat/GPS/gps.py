import smbus
import time
import pynmea2

I2C_BUS = 1
GPS_ADDRESS = 0x42

# Create SMBus Instance
bus = smbus.SMBus(I2C_BUS)


# Record data for lon, lat and time
def recordLog():
    read_lon, read_lat = getLonLat()
    timestamp = time.strftime("%H:%M:%S")
    date = time.strftime("%Y%m%d")
    path = f"./GPS_{date}.log"

    try:
        with open(path, "a", encoding="utf-8") as f:
            f.write(f"{timestamp},{read_lon:08.5f},{read_lat:08.5f}\n")

    except:
        with open(path, "x", encoding="utf-8") as f:
            f.write(f"{timestamp},{read_lon:08.5f},{read_lat:08.5f}\n")


def getLonLat(DEG=False):
    data_nmea = read_data_gps()
    # Separate with newline
    data_nmea_arr = data_nmea.split("\r\n")
    # Dummy data if not received
    read_lon = 00000.00000
    read_lat = 00000.00000
    # read_time = "00:00:00+00:00"

    for index_i in range(len(data_nmea_arr)):
        # print(data_nmea_arr[index_i], end=" ")
        start_index = data_nmea_arr[index_i].find("$") + 3
        end_index = data_nmea_arr[index_i].find(",")
        nmea_cat = data_nmea_arr[index_i][start_index:end_index]
        # print("nmea_cat:",nmea_cat,end="")
        if nmea_cat == "RMC" or nmea_cat == "GGA" or nmea_cat == "GLL":
            try:
                # print("nmea_cat:",nmea_cat,end=", ")
                msg = pynmea2.parse(data_nmea_arr[index_i])
                # print("longitude:",msg.lon,", latitude:", msg.lat)
                read_lon = float(msg.lon)
                read_lat = float(msg.lat)

                if DEG == True:
                    read_lon = dms2deg(read_lon)
                    read_lat = dms2deg(read_lat)

            except Exception as e:
                print("", end="")
        # else:
        # print("<-not include lon,lat")
        # if nmea_cat == "GLL" or time ==:
        #    try:
        #        # print("nmea_cat:",nmea_cat,end=", ")
        #        msg = pynmea2.parse(data_nmea_arr[index_i])
        #        # print("timestamp:",msg.timestamp)
        #        read_time = msg.timestamp
        #    except Exception as e:
        #        print("", end="")

    return read_lon, read_lat


def dms2deg(dms):
    deg = int(dms // 10000)
    min = int((dms % 10000) // 100)
    sec = dms % 100
    decdeg = deg + (min / 60) + (sec / 3600)

    return decdeg


def read_data_gps():
    try:
        rx_data_nmea = ""
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
                    # print(count_FF, len(rx_data_nmea))
                    if count_FF >= 50 and len(rx_data_nmea) >= 1:
                        # print("NoData Period")
                        count_FF = 0
                        check = 1

        return rx_data_nmea

    except Exception as e:
        print("", end="")
        # print(f"Error reading from GPS module: {e}")
        return ""


if __name__ == "__main__":
    while True:
        read_lon, read_lat = getLonLat()
        recordLog()
        print("Longitude:", read_lon, ", Latitude:", read_lat)
        time.sleep(3)
