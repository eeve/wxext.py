#-*- coding:utf-8 -*-
import crython
import datetime
from wxpy import *
from extend import (pm2_5, weather, pcbeta)

# * * * * * * *
# | | | | | | |
# | | | | | | +-- Year              (range: 1900-3000)
# | | | | | +---- Day of the Week   (range: 1-7, 1 standing for Monday)
# | | | | +------ Month of the Year (range: 1-12)
# | | | +-------- Day of the Month  (range: 1-31)
# | | +---------- Hour              (range: 0-23)
# | +------------ Minute            (range: 0-59)
# +-------------- Seconds           (range: 0-59)

global bot

# 每隔30分钟报告空气质量情况
@crython.job(expr='0 */30 * * * * *')
def kongqi():
	bot.self.send(pm2_5.getPM2_5Msg())

# 每天早上8点，报告天气情况
@crython.job(expr='0 0 8 * * * *')
def tianqi():
	bot.self.send(weather.getWeatherMsg())

# 每天早上8点，远景论坛签到任务
@crython.job(expr='0 0 8 * * * *')
def checkInPcbeta():
	bot.self.self('远景签到任务：%s' % pcbeta.qiandao())

if __name__ == '__main__':
	bot = Bot(cache_path=True, console_qr=True)
	crython.start()
	embed()
