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
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp']), math.floor(weather['low']), math.floor(weather['high']), weather['airQuality'], weather['wind']

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
data = {"weather":{"value":"今日天气状况："+ wea},
"temperature":{"value":"当前温度"+ temp},
"low":{"value":"今日最低气温"+ low},
"high":{"value":"今日最高气温 "+ high},
"airQuality":{"value":"空气质量 "+ airQuality},
"wind":{"value":"今日风向 "+  wind},
"love_days":{"value": "今天是在一起的第  "+get_count()+"  天"},
"birthday_left":{"value":"距离生日还有 "+ get_birthday() +"天"},
"words":{"value":get_words(),
"color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
