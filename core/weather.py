# encoding: utf-8

from model import *
from lxml import html
import requests
from voice import Voice


class WeatherProcessor(Processor):
    def __init__(self, tags={'weather'}):
        super(WeatherProcessor, self).__init__(tags)
        self.fr = None
        self.to = None
        self.into = None

    def checkWeather(self, i):
        page = requests.get('http://www.meteoprog.ua/ru/weather/Odesa/#detail')
        tree = html.fromstring(page.text)

        self.fr = tree.xpath('//span[@class="from"]/text()')
        self.to = tree.xpath('//span[@class="to"]/text()')
        self.info = tree.xpath('//div[@class="infoPrognosis widthProg"]/text()')

        # prepare info for the day
        info = self.info[i].encode('utf-8').strip()
        x = info.index(':')
        info = info[x + 1:]
        # prepare day name
        day = 'Сегодня'
        if i == 1:
            day = 'Завтра'
        # prepare string to say
        s = '%s за бортом %s %s, %s' % (day, self.fr[i].encode('utf-8')[:3], self.to[i].encode('utf-8'), info)
        logging.info(s)
        Voice.getInstance().say(s)

    def processCommandByMyself(self, cmd):
        self.checkWeather(0)


class TomorrowWeatherProcessor(WeatherProcessor):
    def __init__(self, tags={'tomorrow'}):
        super(TomorrowWeatherProcessor, self).__init__(tags)

    def processCommandByMyself(self, cmd):
        self.checkWeather(1)
