import logging
import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

import Image
import ImageDraw


class Screen:
    def __init__(self, pin=24):
        logging.debug('Initialize screen')
        self.disp = Adafruit_SSD1306.SSD1306_128_32(rst=pin)
        self.disp.begin()
        self.disp.clear()
        self.disp.display()

        self.width = self.disp.width
        self.height = self.disp.height
        logging.debug('Screen resolution: %sX%s' % (self.width, self.height))

    def draw(self):
        image = Image.new('1', (self.width, self.height))
        draw = ImageDraw.Draw(image)
        draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)
        draw.ellipse((2, 2, 22, self.height - 2), outline=255, fill=0)
        self.disp.image(image)
        self.disp.display()

    def __del__(self):
        self.disp.clear()
        self.disp.display()

if __name__ == 'main':
    s = Screen()
    s.draw()
    time.sleep(3)

