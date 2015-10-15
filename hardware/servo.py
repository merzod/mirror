import RPi.GPIO as GPIO
import utils
import logging


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

        GPIO.setup(pin, GPIO.OUT)
        self.p = GPIO.PWM(pin, 100)
        self.p.start(1)

    # Control the servo. Turn to specified angle.
    def move(self, angle):
        angle = utils.check(angle, self.MIN_ANGLE, self.MAX_ANGLE)
        val = float(angle)*18.0/180.0+5
        logging.debug("Moving Servo angle=%d val=%d" % (angle, val))
        self.p.ChangeDutyCycle(val)

    def __del__(self):
        self.p.stop()

if __name__ == '__main__':
    s = Servo(10)
    s.move(0)
    s.move(90)
    s.move(180)
