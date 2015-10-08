import RPi.GPIO as GPIO
import time
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s\t(%(threadName)-10s) %(filename)s:%(lineno)d\t%(message)s')


class Motor:
    FORWARD = True
    BACKWARD = False
    MIN_SPEED = 15
    MAX_SPEED = 100
    MIN_TIME = 1
    MAX_TIME = 3

    def __init__(self, pin_direct1, pin_direct2, pin_speed):
        logging.debug('Initializing motor with pins (%d, %d, %d)' % (pin_direct1, pin_direct2, pin_speed))
        self.pin_direct1 = pin_direct1
        self.pin_direct2 = pin_direct2
        self.pin_speed = pin_speed

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin_speed, GPIO.OUT)
        self.p = GPIO.PWM(pin_speed, 100)
        GPIO.setup(pin_direct1, GPIO.OUT)
        GPIO.output(pin_direct1, 0)
        GPIO.setup(pin_direct2, GPIO.OUT)
        GPIO.output(pin_direct2, 0)
        self.p.start(1)

    def move(self, direction=FORWARD, period=1, speed=100):
        logging.debug('Moving motor dir=%s time=%d speed=%d' % (direction, period, speed))
        speed = Motor.check(speed, Motor.MIN_SPEED, Motor.MAX_SPEED)
        period = Motor.check(period, Motor.MIN_TIME, Motor.MAX_TIME)
        self.p.ChangeDutyCycle(speed)
        GPIO.output(self.pin_direct1, direction)
        GPIO.output(self.pin_direct2, not direction)
        time.sleep(period)
        logging.debug('Stop motor')
        GPIO.output(self.pin_direct1, 0)
        GPIO.output(self.pin_direct2, 0)

    @staticmethod
    def check(val, min, max):
        if val < min:
            val = min
        if val > max:
            val = max
        return val

    def __del__(self):
        self.p.stop()
        GPIO.cleanup()

m = Motor(33, 35, 37)
m.move()
m.move(Motor.BACKWARD, 2, 20)