import RPi.GPIO as GPIO
import threading
import logging
import servo
import screen
from motor import Motor

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s\t(%(threadName)-10s) %(filename)s:%(lineno)d\t%(message)s')


class Base:
    TURN_LEFT = True
    TURN_RIGHT = False

    LEFT_ARM = True
    RIGHT_ARM = False

    UP = True
    DOWN = False

    FORWARD = Motor.FORWARD
    BACKWARD = Motor.BACKWARD

    HEAD_MOVE_ANGLE = 45

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.left_leg = Motor(26, 19, 13)
        self.right_leg = Motor(16, 20, 21)
        self.head = servo.Servo(17)
        self.head_angle = 90
        self.left_arm = servo.Servo(27, min_angle=0, max_angle=90)
        self.right_arm = servo.Servo(22, min_angle=90, max_angle=180)
        self.face = screen.ScreenWrapper(screen.Screen())
        self.face.draw_walle_state()

    def move(self, direction, period=Motor.DEF_TIME, speed=Motor.DEF_SPEED):
        t1 = threading.Thread(target=self.left_leg.move, args=(direction, period, speed))
        t2 = threading.Thread(target=self.right_leg.move, args=(direction, period, speed))
        t1.start()
        t2.start()

    def turn(self, direction, period=0.1, speed=Motor.DEF_SPEED):
        t1 = threading.Thread(target=self.left_leg.move, args=(not direction, period, speed))
        t2 = threading.Thread(target=self.right_leg.move, args=(direction, period, speed))
        t1.start()
        t2.start()

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
            target = self.right_arm.move

        t = threading.Thread(target=target, args=(angle,))
        t.start()

    def move_head(self, direction):
        old_angle = self.head_angle
        if direction == Base.TURN_LEFT and self.head_angle >= Base.HEAD_MOVE_ANGLE:
            self.head_angle -= Base.HEAD_MOVE_ANGLE
        elif direction == Base.TURN_RIGHT and self.head_angle <= 180 - Base.HEAD_MOVE_ANGLE:
            self.head_angle += Base.HEAD_MOVE_ANGLE
        if old_angle != self.head_angle:
            t = threading.Thread(target=self.head.move, args=(self.head_angle, ))
            t.start()

    def __del__(self):
        GPIO.cleanup()


if __name__ == '__main__':
    base = Base()
    # base.move_arm(Base.LEFT_ARM, Base.UP)
    # base.move_arm(Base.RIGHT_ARM, Base.UP)
    # base.move_arm(Base.LEFT_ARM, Base.DOWN)
    # base.move_arm(Base.RIGHT_ARM, Base.DOWN)
    # for i in range(0, 4):
    #    base.move()
    #    base.turn()
    # base.move(motor.Motor.BACKWARD, period=2)
    # base.turn()
    # base.turn(Base.TURN_RIGHT)
