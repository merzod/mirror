from msvcrt import getch
import logging

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


while True:
    key = ord(getch())
    logging.debug('Pressed: %d' % key)
    if key == ESCAPE:
        break
    elif key == SPECIAL_FLAG: # Special keys (arrows, f keys, ins, del, etc.)
        key = ord(getch())
        logging.debug('Special key: %d' % key)
        if key == MOVE_FORWARD:
            pass
        elif key == MOVE_BACKWARD:
            pass
        elif key == TURN_LEFT:
            pass
        elif key == TURN_RIGHT:
            pass
    elif key == HEAD_LEFT:
        pass
    elif key == HEAD_RIGHT:
        pass
    elif key == LEFT_ARM_UP:
        pass
    elif key == LEFT_ARM_DOWN:
        pass
    elif key == RIGHT_ARM_UP:
        pass
    elif key == RIGHT_ARM_DOWN:
        pass
