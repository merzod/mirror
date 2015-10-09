import motor
import threading
import time


class Base:
    TURN_LEFT = True
    TURN_RIGHT = False

    def __init__(self):
        self.m1 = motor.Motor(33, 35, 37)
        self.m2 = motor.Motor(32, 29, 31)

    def move(self, direction=motor.Motor.FORWARD, period=1, speed=100):
        t1 = threading.Thread(target=self.m1.move, args=(direction, period, speed))
        t2 = threading.Thread(target=self.m2.move, args=(direction, period, speed))
        t1.start()
        t2.start()
        time.sleep(period)

    def turn(self, direction=TURN_LEFT, period=1, speed=100):
        t1 = threading.Thread(target=self.m1.move, args=(not direction, period, speed))
        t2 = threading.Thread(target=self.m2.move, args=(direction, period, speed))
        t1.start()
        t2.start()
        time.sleep(period)

base = Base()
base.move()
base.move(motor.Motor.BACKWARD, period=2)
base.turn()
base.turn(Base.TURN_RIGHT)
