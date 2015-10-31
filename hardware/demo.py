import logging
import time
from base import Base

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s\t(%(threadName)-10s) %(filename)s:%(lineno)d\t%(message)s')

if __name__ == "__name__":
    walle = Base()

    # move forward
    walle.move(Base.FORWARD)
    time.sleep(2)

    # shake hand twice
    direction = Base.DOWN
    for i in range(0, 3):
        direction = not direction
        walle.move_arm(Base.RIGHT_ARM, direction)
        time.sleep(0.3)

    # TODO: say walle
    # TODO: screen demo
    time.sleep(1)

    # turn head
    walle.head.move(0)
    time.sleep(1)
    walle.head.move(180)
    time.sleep(1)

    # turn
    walle.head.move(45)
    walle.turn(Base.TURN_LEFT, 1)
    walle.head.move(90)
    time.sleep(0.5)
    walle.head.move(135)
    walle.turn(Base.TURN_RIGHT, 1)
    walle.head.move(90)
