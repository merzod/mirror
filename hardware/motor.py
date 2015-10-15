import RPi.GPIO as GPIO
import time
import logging
import utils


# Class represents Motor. Hardware motor connected to RPi over L298N motor driver. For initialization 3 pins are used.
# Pin 1, Pin 2 - direction pins; Pin 3 - speed control (PWM)
class Motor:
    FORWARD = True
    BACKWARD = False
    MIN_SPEED = 15
    DEF_SPEED = 100
    MAX_SPEED = 100
    MIN_TIME = 1
    DEF_TIME = 1
    MAX_TIME = 3

    # Motor constructor. Initialize GPIO connector using incoming pins.
    def __init__(self, pin_direct1, pin_direct2, pin_speed):
        logging.debug('Initializing motor with pins (%d, %d, %d)' % (pin_direct1, pin_direct2, pin_speed))
        self.pin_direct1 = pin_direct1
        self.pin_direct2 = pin_direct2
        self.pin_speed = pin_speed

        GPIO.setup(pin_speed, GPIO.OUT)
        self.p = GPIO.PWM(pin_speed, 100)
        GPIO.setup(pin_direct1, GPIO.OUT)
        GPIO.output(pin_direct1, 0)
        GPIO.setup(pin_direct2, GPIO.OUT)
        GPIO.output(pin_direct2, 0)
        self.p.start(1)

    # Control the motor. Used direction, period and speed.
    def move(self, direction=FORWARD, period=DEF_TIME, speed=DEF_SPEED):
        logging.debug('Moving motor dir=%s time=%d speed=%d' % (direction, period, speed))
        speed = utils.check(speed, Motor.MIN_SPEED, Motor.MAX_SPEED)
        period = utils.check(period, Motor.MIN_TIME, Motor.MAX_TIME)
        self.p.ChangeDutyCycle(speed)
        GPIO.output(self.pin_direct1, direction)
        GPIO.output(self.pin_direct2, not direction)
        time.sleep(period)
        logging.debug('Stop motor')
        GPIO.output(self.pin_direct1, 0)
        GPIO.output(self.pin_direct2, 0)

    def __del__(self):
        self.p.stop()
