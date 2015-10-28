import base
from motor import Motor
from base import Base
import logging

class Controller:
    # arrows
    MOVE_FORWARD = 259
    MOVE_BACKWARD = 258
    TURN_LEFT = 260
    TURN_RIGHT = 261

    # '[' and ']'
    HEAD_LEFT = 91
    HEAD_RIGHT = 93

    # q, a, w, s
    LEFT_ARM_UP = 113
    LEFT_ARM_DOWN = 97
    RIGHT_ARM_UP = 119
    RIGHT_ARM_DOWN = 115

    def __init__(self):
        self.walle = base.Base()

    def process(self, code):
        logging.debug('Processing code: %s' % code)
        if code == Controller.MOVE_FORWARD:
            self.walle.move(Motor.FORWARD)
        elif code == Controller.MOVE_BACKWARD:
            self.walle.move(Motor.BACKWARD)
        elif code == Controller.TURN_LEFT:
            self.walle.turn(Base.TURN_LEFT)
        elif code == Controller.TURN_RIGHT:
            self.walle.turn(Base.TURN_RIGHT)
        elif code == Controller.HEAD_LEFT:
            self.walle.move_head(Base.TURN_LEFT)
        elif code == Controller.HEAD_RIGHT:
            self.walle.move_head(Base.TURN_RIGHT)
        elif code == Controller.LEFT_ARM_UP:
            self.walle.move_arm(Base.LEFT_ARM, Base.UP)
        elif code == Controller.LEFT_ARM_DOWN:
            self.walle.move_arm(Base.LEFT_ARM, Base.DOWN)
        elif code == Controller.RIGHT_ARM_UP:
            self.walle.move_arm(Base.RIGHT_ARM, Base.UP)
        elif code == Controller.RIGHT_ARM_DOWN:
            self.walle.move_arm(Base.RIGHT_ARM, Base.DOWN)

    def __del__(self):
        self.walle.__del__()
