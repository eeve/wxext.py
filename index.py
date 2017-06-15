#-*- coding:utf-8 -*-
import crython
import datetime
from wxpy import *
from extend import pm2_5

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

@crython.job(expr='0 */30 * * * * *')
def interval():
  bot.self.send(pm2_5.getPM2_5Msg())


if __name__ == '__main__':
  bot = Bot(cache_path=True, console_qr=True)
  print(bot.friends().stats_text())
  crython.start()
  embed()
