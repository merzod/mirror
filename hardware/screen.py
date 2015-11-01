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

        # title line
        draw.line((64, 1, 126, 1), fill=255)
        draw.line((64, 2, 126, 2), fill=255)

        # sun symbol
        draw.ellipse((64, 4, 85, 16), outline=255, fill=255)
        draw.ellipse((66, 6, 83, 14), outline=255, fill=0)

        # batt level
        for i in range(0, 10):
            x = 12 + i*2
            draw.line((90, x, 126, x), fill=255)
        draw.line((90, 29, 126, 29), fill=255)
        draw.line((90, 31, 126, 31), fill=255)

        self.disp.image(image)
        self.disp.display()

    def draw_img(self):
        image = Image.open('sc.png').resize((self.width, self.height), Image.ANTIALIAS).convert('1')
        self.disp.image(image)
        self.disp.display()

    def __del__(self):
        self.disp.clear()
        self.disp.display()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s\t(%(threadName)-10s) %(filename)s:%(lineno)d\t%(message)s')
    s = Screen()
    s.draw_img()
    time.sleep(3)
