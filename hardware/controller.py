import base
from base import Base
import logging
import sys
sys.path.append('../core/')
from voice import Voice


class Controller:
    # arrows
    MOVE_FORWARD = 259
    MOVE_BACKWARD = 258
    TURN_LEFT = 260
    TURN_RIGHT = 261

    # 'pgup' and 'pgdown'
    HEAD_LEFT = 339
    HEAD_RIGHT = 338

    # q, a, w, s
    LEFT_ARM_UP = 113
    LEFT_ARM_DOWN = 97
    RIGHT_ARM_UP = 119
    RIGHT_ARM_DOWN = 115

    # 1, 2 ...
    SOUND_1 = 49
    SOUND_2 = 50

    def __init__(self):
        self.walle = base.Base()

    def process(self, code):
        logging.debug('Processing code: %s' % code)
        if code == Controller.MOVE_FORWARD:
            self.walle.move(Base.FORWARD)
        elif code == Controller.MOVE_BACKWARD:
            self.walle.move(Base.BACKWARD)
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
        elif code == Controller.SOUND_1:
            Voice.getInstance().playFile('../resources/wall-e.ogg')
        elif code == Controller.SOUND_2:
            Voice.getInstance().playFile('../resources/eve.ogg')

    def __del__(self):
        self.walle.__del__()
