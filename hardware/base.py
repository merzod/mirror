import RPi.GPIO as GPIO
import motor
import threading
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s\t(%(threadName)-10s) %(filename)s:%(lineno)d\t%(message)s')


class Base:
    TURN_LEFT = True
    TURN_RIGHT = False

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        self.m1 = motor.Motor(33, 35, 37)
        self.m2 = motor.Motor(32, 29, 31)

    def move(self, direction=motor.Motor.FORWARD, period=motor.Motor.DEF_TIME, speed=motor.Motor.DEF_SPEED):
        t1 = threading.Thread(target=self.m1.move, args=(direction, period, speed))
        t2 = threading.Thread(target=self.m2.move, args=(direction, period, speed))
        t1.start()
        t2.start()
        t1.join()
        t2.join()

    def turn(self, direction=TURN_LEFT, period=motor.Motor.DEF_TIME, speed=motor.Motor.DEF_SPEED):
        t1 = threading.Thread(target=self.m1.move, args=(not direction, period, speed))
        t2 = threading.Thread(target=self.m2.move, args=(direction, period, speed))
        t1.start()
        t2.start()
        t1.join()
        t2.join()

    def __del__(self):
        GPIO.cleanup()

base = Base()
base.move()
base.move(motor.Motor.BACKWARD, period=2)
base.turn()
base.turn(Base.TURN_RIGHT)
