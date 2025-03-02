import time

# import multiprocessing
import phase1
import phase2
import phase3
#add phase4
import phase4 as phase4


def stamp(start):
    timestamp = start - time.time()
    timestamp = time.strftime("%H:%M:%S", time.gmtime(timestamp))
    return timestamp


start = time.time()

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
