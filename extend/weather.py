#-*- coding:utf-8 -*-
import requests
import time

def getWeatherMsg():
  r = requests.get(url='http://api.k780.com/?app=weather.future&weaid=1&&appkey=10003&sign=b59bc3ef6191eb9f747dd4e83c99f2a4&format=json')
  if( r is None or r.status_code != 200 ):
    return None
  res = r.json()
  if( res.get('success') != '1' ):
    return None
  result = res.get('result')[0]
  return '[{}] 今日天气情况: {} 气温最低({}℃)，最高({}℃)，风向({}), 风力({})'.format(
    result.get('days'),
    result.get('weather'),
    result.get('temp_low'),
    result.get('temp_high'),
    result.get('wind'),
    result.get('winp')
  )

if __name__ == '__main__':
  print(getWeatherMsg())
