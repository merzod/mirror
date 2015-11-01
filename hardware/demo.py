import logging
import time
from base import Base
import sys
sys.path.append('../core/')
from voice import Voice

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s\t(%(threadName)-10s) %(filename)s:%(lineno)d\t%(message)s')

if __name__ == "__main__":
    walle = Base()

    # move forward
    walle.move(Base.FORWARD)
    time.sleep(2)

    # shake hand twice
    direction = Base.DOWN
    for i in range(0, 4):
        direction = not direction
        walle.move_arm(Base.RIGHT_ARM, direction)
        time.sleep(0.3)
    Voice.getInstance().playFile('../resources/wall-e.ogg')

    # screen demo
    frames = [["../resources/anim1/sc0.png", 1],
           ["../resources/anim1/sc1.png", 0.1],
           ["../resources/anim1/sc2.png", 0.5],
           ["../resources/anim1/sc1.png", 0.1],
           ["../resources/anim1/sc0.png", 1]]
    walle.face.play(frames)
    walle.face.state()

    # turn head
    walle.head.move(0)
    time.sleep(1)
    walle.head.move(180)
    time.sleep(1)
    walle.head.move(90)
    time.sleep(1)

    # turn
    walle.head.move(0)
    walle.turn(Base.TURN_LEFT, 1)
    time.sleep(0.2)
    walle.head.move(90)
    time.sleep(1)
    walle.head.move(180)
    walle.turn(Base.TURN_RIGHT, 1)
    time.sleep(0.2)
    walle.head.move(90)
    time.sleep(2)
