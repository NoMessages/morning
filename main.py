from datetime import date, datetime

import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = "2020-11-25"
city = os.environ['CITY']
birthday = "11-02"

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = "http://t.weather.itboy.net/api/weather/city/101280800"
  res = requests.get(url).json()
  detail_info = res['data']
  weather = res['data']['forecast'][0]
  return weather['type'], detail_info['wendu'], math.floor(weather['low']), math.floor(weather['high']), weather['aqi'], weather['fl']

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  return "中午不知道吃啥？菜单参考：-----》\n【红烧肉】【蒜香油麦菜】【爆炒午餐肉】【炝拌干豆腐丝】【鱼香肉丝】【番茄炒蛋】【茄子炒肉沫】【韭菜炒蛋】【酱烧豆腐】【排骨饭】"

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temp, low, high, airQuality, wind = get_weather()
data = {"weather":{"value":wea},
"temperature":{"value":temp},
"low":{"value":low},
"high":{"value":high},
"airQuality":{"value":airQuality},
"wind":{"value": wind},
"love_days":{"value":get_count()},
"birthday_left":{"value":get_birthday()},
"words":{"value":get_words(),
"color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
