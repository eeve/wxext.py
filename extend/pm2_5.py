#-*- coding:utf-8 -*-
import requests
import time

def getPM2_5Msg():
  r = requests.get(url="http://api.k780.com/?app=weather.pm25&weaid=1&appkey=10003&sign=b59bc3ef6191eb9f747dd4e83c99f2a4&format=json")
  if( r is None or r.status_code != 200 ):
    return None
  res = r.json()
  if( res.get('success') != '1' ):
    return None
  result = res.get('result')
  return '[{}] {}实时空气质量 {} ({}) {}, {}'.format(
    time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),
    result.get("citynm"),
    result.get("aqi"),
    result.get("aqi_scope"),
    result.get("aqi_levnm"),
    result.get("aqi_remark")
  )

if __name__ == '__main__':
  print(getPM2_5Msg())

# http://www.pm25.in/api/querys/pm2_5.json?token=5j1znBVAsnSf5xQyNQyq&city=beijing
# [{"aqi":114,"area":"北京","pm2_5":18,"pm2_5_24h":34,"position_name":"万寿西宫","primary_pollutant":"臭氧1小时","quality":"轻度污染","station_code":"1001A","time_point":"2017-06-15T13:00:00Z"},{"aqi":72,"area":"北京","pm2_5":26,"pm2_5_24h":21,"position_name":"定陵","primary_pollutant":"臭氧1小时","quality":"良","station_code":"1002A","time_point":"2017-06-15T13:00:00Z"},{"aqi":94,"area":"北京","pm2_5":70,"pm2_5_24h":37,"position_name":"东四","primary_pollutant":"细颗粒物(PM2.5)","quality":"良","station_code":"1003A","time_point":"2017-06-15T13:00:00Z"},{"aqi":108,"area":"北京","pm2_5":35,"pm2_5_24h":34,"position_name":"天坛","primary_pollutant":"臭氧1小时","quality":"轻度污染","station_code":"1004A","time_point":"2017-06-15T13:00:00Z"},{"aqi":108,"area":"北京","pm2_5":44,"pm2_5_24h":35,"position_name":"农展馆","primary_pollutant":"臭氧1小时","quality":"轻度污染","station_code":"1005A","time_point":"2017-06-15T13:00:00Z"},{"aqi":117,"area":"北京","pm2_5":42,"pm2_5_24h":32,"position_name":"官园","primary_pollutant":"臭氧1小时","quality":"轻度污染","station_code":"1006A","time_point":"2017-06-15T13:00:00Z"},{"aqi":97,"area":"北京","pm2_5":52,"pm2_5_24h":31,"position_name":"海淀区万柳","primary_pollutant":"臭氧1小时","quality":"良","station_code":"1007A","time_point":"2017-06-15T13:00:00Z"},{"aqi":113,"area":"北京","pm2_5":29,"pm2_5_24h":28,"position_name":"顺义新城","primary_pollutant":"臭氧1小时","quality":"轻度污染","station_code":"1008A","time_point":"2017-06-15T13:00:00Z"},{"aqi":110,"area":"北京","pm2_5":19,"pm2_5_24h":20,"position_name":"怀柔镇","primary_pollutant":"臭氧1小时","quality":"轻度污染","station_code":"1009A","time_point":"2017-06-15T13:00:00Z"},{"aqi":94,"area":"北京","pm2_5":24,"pm2_5_24h":23,"position_name":"昌平镇","primary_pollutant":"臭氧1小时","quality":"良","station_code":"1010A","time_point":"2017-06-15T13:00:00Z"},{"aqi":90,"area":"北京","pm2_5":33,"pm2_5_24h":27,"position_name":"奥体中心","primary_pollutant":"臭氧1小时","quality":"良","station_code":"1011A","time_point":"2017-06-15T13:00:00Z"},{"aqi":116,"area":"北京","pm2_5":31,"pm2_5_24h":39,"position_name":"古城","primary_pollutant":"臭氧1小时","quality":"轻度污染","station_code":"1012A","time_point":"2017-06-15T13:00:00Z"},{"aqi":106,"area":"北京","pm2_5":35,"pm2_5_24h":30,"position_name":null,"primary_pollutant":"臭氧1小时","quality":"轻度污染","station_code":null,"time_point":"2017-06-15T13:00:00Z"}]
