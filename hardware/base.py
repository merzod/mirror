import RPi.GPIO as GPIO
import motor
import threading
import logging
import servo
import screen
import time

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s\t(%(threadName)-10s) %(filename)s:%(lineno)d\t%(message)s')


class Base:
    TURN_LEFT = True
    TURN_RIGHT = False

    LEFT_ARM = True
    RIGHT_ARM = False

    UP = True
    DOWN = False

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        self.left_leg = motor.Motor(33, 35, 37)
        self.right_leg = motor.Motor(32, 29, 31)
        self.head = servo.Servo(11)
        self.left_arm = servo.Servo(13, min_angle=0, max_angle=90)
        self.right_arm = servo.Servo(15, min_angle=90, max_angle=180)
        self.face = screen.Screen()
        self.face.draw()


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

    def move_arm(self, arm, position):
        # select the angle, UP for both arms is 90 degrees. down is 0 for left arm and 180 for right one
        angle = 90
        if position == Base.DOWN:
            if arm == Base.LEFT_ARM:
                angle = 0
            elif arm == Base.RIGHT_ARM:
                angle = 180

        # select the arm
        target = None
        if arm == Base.LEFT_ARM:
            target = self.left_arm.move
        elif arm == Base.RIGHT_ARM:
            target = self.right_arm

        t1 = threading.Thread(target=target, args=(angle, ))
        t1.start()
        time.sleep(3)


    def __del__(self):
        GPIO.cleanup()

if __name__ == '__main__':
    base = Base()
    base.move_arm(Base.LEFT_ARM, Base.UP)
    base.move_arm(Base.RIGHT_ARM, Base.UP)
    base.move_arm(Base.LEFT_ARM, Base.DOWN)
    base.move_arm(Base.RIGHT_ARM, Base.DOWN)
    time.sleep(5)
    # base.move()
    # base.move(motor.Motor.BACKWARD, period=2)
    # base.turn()
    # base.turn(Base.TURN_RIGHT)

