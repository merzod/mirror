import RPi.GPIO as GPIO
import utils
import logging
import time


# Class represents Servo. Hardware servo connected to PRi with single signal wire.
class Servo:
    MIN_ANGLE = 0
    MAX_ANGLE = 180

    # Servo constructor. Initialize GPIO connector. Also one can limit servo angles
    def __init__(self, pin, min_angle=MIN_ANGLE, max_angle=MAX_ANGLE):
        logging.debug('Initializing servo with pin %d' % pin)
        self.pin = pin
        self.min_angle = min_angle
        self.max_angle = max_angle

        GPIO.setup(self.pin, GPIO.OUT)
        self.p = GPIO.PWM(self.pin, 100)

    # Control the servo. Turn to specified angle.
    def move(self, angle):
        angle = utils.check(angle, self.MIN_ANGLE, self.MAX_ANGLE)
        val = float(angle) * 18.0 / 180.0 + 5
        logging.debug("Moving Servo angle=%d val=%d" % (angle, val))
        self.p.start(val)
        time.sleep(1)
        self.p.stop()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s\t(%(threadName)-10s) %(filename)s:%(lineno)d\t%(message)s')
    GPIO.setmode(GPIO.BOARD)
    s = Servo(11)
    s.move(0)
    s.move(90)
    s.move(180)
