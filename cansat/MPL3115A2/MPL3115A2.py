import time
import smbus


class MPL3115A2exception(Exception):
    pass


class MPL3115A2:
    ALTITUDE_MODE = 0
    PRESSURE_MODE = 1

    MPL3115_I2CADDR = 0x60
    MPL3115_STATUS = 0x00
    MPL3115_PRESSURE_DATA_MSB = 0x01
    MPL3115_PRESSURE_DATA_CSB = 0x02
    MPL3115_PRESSURE_DATA_LSB = 0x03
    MPL3115_TEMP_DATA_MSB = 0x04
    MPL3115_TEMP_DATA_LSB = 0x05
    MPL3115_DR_STATUS = 0x06
    MPL3115_DELTA_DATA = 0x07
    MPL3115_WHO_AM_I = 0x0C
    MPL3115_FIFO_STATUS = 0x0D
    MPL3115_FIFO_DATA = 0x0E
    MPL3115_FIFO_SETUP = 0x0E
    MPL3115_TIME_DELAY = 0x10
    MPL3115_SYS_MODE = 0x11
    MPL3115_INT_SORCE = 0x12
    MPL3115_PT_DATA_CFG = 0x13
    MPL3115_BAR_IN_MSB = 0x14
    MPL3115_P_ARLARM_MSB = 0x16
    MPL3115_T_ARLARM = 0x18
    MPL3115_P_ARLARM_WND_MSB = 0x19
    MPL3115_T_ARLARM_WND = 0x1B
    MPL3115_P_MIN_DATA = 0x1C
    MPL3115_T_MIN_DATA = 0x1F
    MPL3115_P_MAX_DATA = 0x21
    MPL3115_T_MAX_DATA = 0x24
    MPL3115_CTRL_REG1 = 0x26
    MPL3115_CTRL_REG2 = 0x27
    MPL3115_CTRL_REG3 = 0x28
    MPL3115_CTRL_REG4 = 0x29
    MPL3115_CTRL_REG5 = 0x2A
    MPL3115_OFFSET_P = 0x2B
    MPL3115_OFFSET_T = 0x2C
    MPL3115_OFFSET_H = 0x2D

    def __init__(self, mode):

        self.mode = mode
        self.bus = smbus.SMBus(1)

        if self.mode == MPL3115A2.PRESSURE_MODE:
            # barometer mode, not raw, oversampling 128, minimum time 512 ms
            self.bus.write_byte_data(
                MPL3115A2.MPL3115_I2CADDR, MPL3115A2.MPL3115_CTRL_REG1, 0x38
            )
            self.bus.write_byte_data(
                MPL3115A2.MPL3115_I2CADDR, MPL3115A2.MPL3115_PT_DATA_CFG, 0x07
            )  # no events detected
            self.bus.write_byte_data(
                MPL3115A2.MPL3115_I2CADDR, MPL3115A2.MPL3115_CTRL_REG1, 0x39
            )  # active
        elif self.mode == MPL3115A2.ALTITUDE_MODE:
            # altitude mode, not raw, oversampling 128, minimum time 512 ms
            self.bus.write_byte_data(
                MPL3115A2.MPL3115_I2CADDR, MPL3115A2.MPL3115_CTRL_REG1, 0xB8
            )
            self.bus.write_byte_data(
                MPL3115A2.MPL3115_I2CADDR, MPL3115A2.MPL3115_PT_DATA_CFG, 0x07
            )  # no events detected
            self.bus.write_byte_data(
                MPL3115A2.MPL3115_I2CADDR, MPL3115A2.MPL3115_CTRL_REG1, 0xB9
            )  # active
        else:
            raise MPL3115A2exception("Invalid Mode MPL3115A2")

    def getPressure(self):
        if self.mode == MPL3115A2.ALTITUDE_MODE:
            raise MPL3115A2exception("Incorrect Measurement Mode MPL3115A2")

        out_pressure = self.bus.read_i2c_block_data(
            MPL3115A2.MPL3115_I2CADDR, MPL3115A2.MPL3115_PRESSURE_DATA_MSB, 3
        )

        pressure_int = (
            (out_pressure[0] << 10)
            + (out_pressure[1] << 2)
            + ((out_pressure[2] >> 6) & 0x3)
        )
        pressure_frac = (out_pressure[2] >> 4) & 0x03

        return float(pressure_int + pressure_frac / 4.0)

    def getAltitude(self):
        if self.mode == MPL3115A2.PRESSURE_MODE:
            raise MPL3115A2exception("Incorrect Measurement Mode MPL3115A2")

        out_alt = self.bus.read_i2c_block_data(
            MPL3115A2.MPL3115_I2CADDR, MPL3115A2.MPL3115_PRESSURE_DATA_MSB, 3
        )

        alt_int = (out_alt[0] << 8) + (out_alt[1])
        alt_frac = (out_alt[2] >> 4) & 0x0F

        if alt_int > 32767:
            alt_int -= 65536

        return float(alt_int + alt_frac / 16.0)

    def getTemperature(self):
        OUT_T_MSB = self.bus.read_i2c_block_data(
            MPL3115A2.MPL3115_I2CADDR, MPL3115A2.MPL3115_TEMP_DATA_MSB, 1
        )
        OUT_T_LSB = self.bus.read_i2c_block_data(
            MPL3115A2.MPL3115_I2CADDR, MPL3115A2.MPL3115_TEMP_DATA_LSB, 1
        )

        temp_int = OUT_T_MSB[0]
        temp_frac = OUT_T_LSB[0]

        if temp_int > 127:
            temp_int -= 256

        return float(temp_int + temp_frac / 256.0)

    def recordLog(self):
        timestamp = time.strftime("%H:%M:%S")
        date = time.strftime("%Y%m%d")
        path = f"./MPL3115A2_{date}.log"

        if self.mode == self.ALTITUDE_MODE:#self.MPL3115A2.ALTITUDE_MODE was modified by kawako
            buf = self.getAltitude()

        elif self.mode == self.PRESSURE_MODE:#self.MPL3115A2.PRESSURE_MODE was modified by kawako
            buf = self.getPressure()

        else:
            raise MPL3115A2exception("Incorrect Measurement Mode MPL3115A2")

        try:
            with open(path, "x", encoding="utf-8") as f:
                f.write(f"{timestamp},{buf}\n")

        except:
            with open(path, "a", encoding="utf-8") as f:
                f.write(f"{timestamp},{buf}\n")


if __name__ == "__main__":
    mpla = MPL3115A2(MPL3115A2.ALTITUDE_MODE)
    mplp = MPL3115A2(MPL3115A2.PRESSURE_MODE)

    while True:
        mpla.recordLog()
        altitude = mpla.getAltitude()
        temperature = mpla.getTemperature()
        pressure = mplp.getPressure()

        print("Pressure : %.2f Pa" % pressure)
        print("Altitude : %.2f m" % altitude)
        print("Temperature : %.2f C" % temperature)
        time.sleep(1)
