import logging
from base import Base
from motor import Motor
import curses

stdscr = curses.initscr()
stdscr.noecho()
stdscr.cbreak()
stdscr.keypad(1)

ESCAPE = 27
SPECIAL_FLAG = 224

# arrows
MOVE_FORWARD = 72
MOVE_BACKWARD = 80
TURN_LEFT = 75
TURN_RIGHT = 77

# '[' and ']'
HEAD_LEFT = 91
HEAD_RIGHT = 93

# q, a, w, s
LEFT_ARM_UP = 113
LEFT_ARM_DOWN = 97
RIGHT_ARM_UP = 119
RIGHT_ARM_DOWN = 115

walle = Base()

while True:
    key = stdscr.getch()
    logging.debug('Pressed: %d' % key)
    if key == ESCAPE:
        break
    elif key == MOVE_FORWARD:
        walle.move(Motor.FORWARD)
    elif key == MOVE_BACKWARD:
        walle.move(Motor.BACKWARD)
    elif key == TURN_LEFT:
        walle.turn(Base.TURN_LEFT)
    elif key == TURN_RIGHT:
        walle.turn(Base.TURN_RIGHT)
    elif key == HEAD_LEFT:
        walle.move_head(Base.TURN_LEFT)
    elif key == HEAD_RIGHT:
        walle.move_head(Base.TURN_RIGHT)
    elif key == LEFT_ARM_UP:
        walle.move_arm(Base.LEFT_ARM, Base.UP)
    elif key == LEFT_ARM_DOWN:
        walle.move_arm(Base.LEFT_ARM, Base.DOWN)
    elif key == RIGHT_ARM_UP:
        walle.move_arm(Base.RIGHT_ARM, Base.UP)
    elif key == RIGHT_ARM_DOWN:
        walle.move_arm(Base.RIGHT_ARM, Base.DOWN)
