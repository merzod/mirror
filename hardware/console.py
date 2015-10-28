import logging
import curses
from controller import Controller

stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(1)

ESCAPE = 27

controller = Controller()

while True:
    key = stdscr.getch()
    logging.debug('Pressed: %d' % key)
    if key == ESCAPE:
        break
    controller.process(key)

curses.nocbreak()
stdscr.keypad(0)
curses.echo()
curses.endwin()
