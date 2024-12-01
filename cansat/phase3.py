from Router import router
from Motor import robot
import time


def phase3(goal_pos):
    rt = router.Router(goal_pos)
    while not rt.isGoal():
        times = 0
        rt.start()
        time.sleep(1)
        deg = rt.getAngleDiff()

        while abs(deg) > 15 and times < 5:
            robot.turn(deg)
            deg = rt.getAngleDiff()
            times += 1

        robot.move(0.75, 10)
        robot.stop()
        rt.stop()

    print("Arrived!!")

if __name__ == "__main__":
    goal_pos = [139.5182666, 35.463201]
    phase3(goal_pos)
