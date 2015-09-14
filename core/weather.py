# encoding: utf-8

from model import *
from lxml import html
import requests
from voice import Voice


# Base weather processor, show today's weather
class WeatherProcessor(Processor):
    def __init__(self, tags={'погод', 'борто'}):
        super(WeatherProcessor, self).__init__(tags)

    # check weather for specified day and say it
    def checkWeather(self, i):
        page = requests.get('http://www.meteoprog.ua/ru/weather/Odesa/#detail')
        tree = html.fromstring(page.text)

        fr = tree.xpath('//span[@class="from"]/text()')
        to = tree.xpath('//span[@class="to"]/text()')
        info = tree.xpath('//div[@class="infoPrognosis widthProg"]/text()')

        # prepare info for the day
        info = info[i].encode('utf-8').strip()
        x = info.index(':')
        info = info[x + 1:]
        # prepare day name
        day = 'Сегодня'
        if i == 1:
            day = 'Завтра'
        # prepare string to say
        s = '%s за бортом %s %s, %s' % (day, fr[i].encode('utf-8')[:3], to[i].encode('utf-8'), info)
        logging.info(s)
        Voice.getInstance().say(s)

    def processCommandByMyself(self, cmd):
        self.checkWeather(0)


# Tomorrow weather processor
class TomorrowWeatherProcessor(WeatherProcessor):
    def __init__(self, tags={'завтра'}):
        super(TomorrowWeatherProcessor, self).__init__(tags)

    def processCommandByMyself(self, cmd):
        self.checkWeather(1)
