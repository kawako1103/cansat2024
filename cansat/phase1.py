import time
import timeout_decorator

from BNO055 import BNO055
from MPL3115A2 import MPL3115A2


@timeout_decorator.timeout(3600)
def phase1():
    mpl = MPL3115A2.MPL3115A2(0)
    bno = BNO055.BNO055()
    bno.begin()
    time.sleep(1)
    bno.setExternalCrystalUse(True)

    checkpoint = [False, False, False]
    alt = 0
    alt0 = 0
    while alt0 == 0:
        alt0 = mpl.getAltitude()
    acc = 0
    acc0 = 15
    alt_upth = alt0 + 1.0#2000
    alt_lowth = alt0 + 0.2#10
    counter = 0
    stop_time = 100

    while True:
        alt = mpl.getAltitude()
        acc = bno.getABSAccelaration()
        print("alt", alt)
        print("acc", acc)
        print(checkpoint.count(True))

        # Check Point 1: Check if the upper threshold is exceeded
        if (alt > alt_upth) and checkpoint.count(True) == 0:
            checkpoint[0] = True
            print("Done check0")

        # Check Point 2: Check if the lower threshold is exceeded
        if (alt < alt_lowth) and checkpoint.count(True) == 1:
            checkpoint[1] = True
            print("Done check1")

        # Check Point 3: Check if the rocer is stop
        if (acc < acc0) ^ checkpoint.count(True) == 2:
            counter += 1
            if counter > stop_time:
                checkpoint[2] = True
                print("Done check2")

        # Check if all checkpoint finished
        if all(checkpoint):
            print("Done Phase1")
            return

        time.sleep(0.05)


if __name__ == "__main__":
    phase1()
