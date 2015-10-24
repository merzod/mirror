import RPi.GPIO as GPIO
import motor
import threading
import logging
import servo
import screen

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s\t(%(threadName)-10s) %(filename)s:%(lineno)d\t%(message)s')


class Base:
    TURN_LEFT = True
    TURN_RIGHT = False

    ARM_LEFT = True
    ARM_RIGHT = False

    UP = True
    DOWN = False

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        self.left_leg = motor.Motor(33, 35, 37)
        self.right_leg = motor.Motor(32, 29, 31)
        self.head = servo.Servo(11)
        self.left_arm = servo.Servo(13)
        self.right_arm = servo.Servo(15)
        self.face = screen.Screen()


    def move(self, direction=motor.Motor.FORWARD, period=motor.Motor.DEF_TIME, speed=motor.Motor.DEF_SPEED):
        t1 = threading.Thread(target=self.left_leg.move, args=(direction, period, speed))
        t2 = threading.Thread(target=self.right_leg.move, args=(direction, period, speed))
        t1.start()
        t2.start()
        t1.join()
        t2.join()

    def turn(self, direction=TURN_LEFT, period=motor.Motor.DEF_TIME, speed=motor.Motor.DEF_SPEED):
        t1 = threading.Thread(target=self.left_leg.move, args=(not direction, period, speed))
        t2 = threading.Thread(target=self.right_leg.move, args=(direction, period, speed))
        t1.start()
        t2.start()
        t1.join()
        t2.join()

    def __del__(self):
        GPIO.cleanup()

if __name__ == '__main__':
    base = Base()
    # base.move()
    # base.move(motor.Motor.BACKWARD, period=2)
    # base.turn()
    # base.turn(Base.TURN_RIGHT)

