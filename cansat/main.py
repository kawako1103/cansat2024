import time
import sys
import os

import threading

##
# sys.path.append(os.path.abspath("/LoRa/lora_tx_release_pre2"))
# from lora_tx_release_pre2 import LoRaTransmitter
## 
# from LoRa import lora_tx_release_pre2
from LoRa.lora_tx_release_pre2 import lora_tx_release_pre2
# 

# import multiprocessing
import phase1
import phase2
import phase3_1 as phase3
#add phase4
import phase4 as phase4


goal_pos = [139.514296921, 35.461619311]


def stamp(start):
    timestamp = start - time.time()
    timestamp = time.strftime("%H:%M:%S", time.gmtime(timestamp))
    return timestamp


start = time.time()

##03031923
# LoRa in thread
lora_thread = threading.Thread(target=lora_tx_release_pre2)
lora_thread.start()
# lora_tx_release_pre2()
##

phase1.phase1()
phase1_time = stamp(start)
print(f"Time taken for Phase 1: {phase1_time}")

phase2.phase2()
phase2_time = stamp(start)
print(f"Time taken for Phase 2: {phase2_time}s")

phase3.phase3(goal_pos)
phase3_time = stamp(start)
print(f"Time taken for Phase 3: {phase3_time}s")

#add phase4
phase4.phase4()
phase4_time = stamp(start)
print(f"Time taken for Phase 4: {phase4_time}s")

# wait for LoRa thread 
lora_thread.join()

