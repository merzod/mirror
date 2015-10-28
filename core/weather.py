# encoding: utf-8

from model import *
from lxml import html
import requests
from voice import Voice


# Base weather processor, show today's weather
class WeatherProcessor(Processor):
    def __init__(self, tags={'погод', 'борто', 'улиц'}):
        super(WeatherProcessor, self).__init__(tags)

    # check weather for specified day and say it
    def checkWeather(self, day):
        page = requests.get('http://www.meteoprog.ua/ru/weather/Odesa/#detail')
        tree = html.fromstring(page.text)
        s = self.prepareString(tree, day)
        logging.info(s)
        Voice.getInstance().say(s)

    def prepareString(self, tree, day):
        fr = tree.xpath('//span[@class="from"]/text()')
        to = tree.xpath('//span[@class="to"]/text()')
        info = tree.xpath('//div[@class="infoPrognosis widthProg"]/text()')

        # prepare info for the day
        infoStr = info[day].encode('utf-8').strip()
        x = infoStr.index(':')
        infoStr = infoStr[x + 1:]
        # prepare day name
        dayStr = 'Сегодня'
        if day == 1:
            dayStr = 'Завтра'
        # prepare string to say
        return '%s за бортом %s %s, %s' % (dayStr, fr[day].encode('utf-8')[:3], to[day].encode('utf-8'), infoStr)

    def processCommandByMyself(self, cmd):
        self.checkWeather(0)


# Tomorrow weather processor
class TomorrowWeatherProcessor(WeatherProcessor):
    def __init__(self, tags={'завтра'}):
        super(TomorrowWeatherProcessor, self).__init__(tags)

    def processCommandByMyself(self, cmd):
        self.checkWeather(1)


# Right now weather processor
class NowWeatherProcessor(WeatherProcessor):
    def __init__(self, tags={'сейчас'}):
        super(NowWeatherProcessor, self).__init__(tags)

    def processCommandByMyself(self, cmd):
        self.checkWeather(0)

    def prepareString(self, tree, day):
        info = tree.xpath('//img[@class="avatar-img"]/@title')[0].encode('utf-8').strip()
        x = info.index(':')
        info = info[x + 1:]
        return 'Сейчас %s' % info

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s\t(%(threadName)-10s) %(filename)s:%(lineno)d\t%(message)s')
    wp = WeatherProcessor()
    wp.checkWeather(0)