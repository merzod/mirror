import logging
import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

import Image
import ImageDraw
import ImageFont
import threading


class Screen(object):
    def __init__(self, pin=24):
        logging.debug('Initialize screen')
        self.disp = Adafruit_SSD1306.SSD1306_128_32(rst=pin)
        self.disp.begin()
        self.disp.clear()
        self.disp.display()

        self.width = self.disp.width
        self.height = self.disp.height
        logging.debug('Screen resolution: %sX%s' % (self.width, self.height))

    def __del__(self):
        self.disp.clear()
        self.disp.display()


class ScreenWrapper(object):
    instance = None

    def __init__(self, screen):
        self.screen = screen
        self.lock = threading.Lock

    def __del__(self):
        del self.screen

    @staticmethod
    def getInstance():
        if ScreenWrapper.instance is None:
            ScreenWrapper.instance = ScreenWrapper(Screen())
        return ScreenWrapper.instance

    def cleanup(self):
        self.lock.acquire()
        image = Image.new('1', (self.screen.width, self.screen.height))
        draw = ImageDraw.Draw(image)
        draw.rectangle((0, 0, self.screen.width, self.screen.height), outline=0, fill=0)
        self.screen.disp.image(image)
        self.screen.disp.display()
        self.lock.release()

    def draw_processing(self):
        self.lock.acquire()
        image = Image.new('1', (self.screen.width, self.screen.height))
        draw = ImageDraw.Draw(image)
        self.fill_walle_state(draw)
        draw.rectangle((0, 29, 10, 32), outline=255, fill=255)
        self.screen.disp.image(image)
        self.screen.disp.display()
        self.lock.release()


    def draw_walle_state(self):
        self.lock.acquire()
        image = Image.new('1', (self.screen.width, self.screen.height))
        draw = ImageDraw.Draw(image)
        self.fill_walle_state(draw)
        self.screen.disp.image(image)
        self.screen.disp.display()
        self.lock.release()

    def fill_walle_state(self, draw):
        self.lock.acquire()
        draw.rectangle((0, 0, self.screen.width, self.screen.height), outline=0, fill=0)

        # title line
        draw.line((64, 1, 126, 1), fill=255)
        draw.line((64, 2, 126, 2), fill=255)

        # sun symbol
        draw.ellipse((64, 4, 85, 16), outline=255, fill=255)
        draw.ellipse((66, 6, 83, 14), outline=255, fill=0)

        # batt level
        for i in range(0, 10):
            x = 12 + i * 2
            draw.line((90, x, 126, x), fill=255)
        draw.line((90, 29, 126, 29), fill=255)
        draw.line((90, 31, 126, 31), fill=255)
        self.lock.release()

    def draw_file(self, name):
        self.lock.acquire()
        image = Image.open(name).resize((self.screen.width, self.screen.height), Image.ANTIALIAS).convert('1')
        self.screen.disp.image(image)
        self.screen.disp.display()
        self.lock.release()

    def play(self, frames):
        self.lock.acquire()
        for frame in frames:
            self.draw_file(frame[0])
            time.sleep(frame[1])
        self.lock.release()

    def write(self, text, x=0, y=0, size=8):
        self.lock.acquire()
        image = Image.new('1', (self.screen.width, self.screen.height))
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype('../resources/font/VCR_OSD_MONO_1.001.ttf', size)
        draw.text((x, y), text, font=font, fill=255)
        self.screen.disp.image(image)
        self.screen.disp.display()
        self.lock.release()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s\t(%(threadName)-10s) %(filename)s:%(lineno)d\t%(message)s')
    # frames1 = [["../resources/anim1/sc0.png", 1],
    #            ["../resources/anim1/sc1.png", 0.1],
    #            ["../resources/anim1/sc2.png", 0.5],
    #            ["../resources/anim1/sc1.png", 0.1],
    #            ["../resources/anim1/sc0.png", 1]]
    # s.play(frames1)

    ScreenWrapper.getInstance().write('+20 +24', size=30)
    time.sleep(3)
    ScreenWrapper.getInstance().cleanup()
    del ScreenWrapper.instance
