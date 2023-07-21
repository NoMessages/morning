import _datetime
import sxtwl
from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

def get_cele_date():
  next = datetime.strptime(str(date.today().year) + "-" + "11-25", "%Y-%m-%d")
  if next <= datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - nowTime).days

def get_week_day(date):
    week_day_dict = {
        0: '星期一',
        1: '星期二',
        2: '星期三',
        3: '星期四',
        4: '星期五',
        5: '星期六',
        6: '星期天',
    }
    day = date.weekday()
    return week_day_dict[day]


def get_total_year():
  next = datetime.strptime(str(date.today().year) + "-" + "11-25", "%Y-%m-%d")
  if next <= datetime.now():
    next = next.replace(year=next.year + 1)
  return (next.year - 2020) - 1

# 获取下次生日
def get_next_birthday(nowTime,birthday,remind_calendar):
    if remind_calendar == 1:
        nextYear = nowTime.year
        if nowTime.month>birthday.month or (nowTime.month == birthday.month and nowTime.day > birthday.day):
            nextYear += 1
        isRun = nextYear%4==0 and nextYear%100 != 0 or nextYear % 400==0
        if birthday.month == 2 and birthday.day == 29 and not isRun:
            while not isRun:
                nextYear += 1
                isRun = nextYear%4==0 and nextYear%100 != 0 or nextYear % 400==0
        return datetime(year = nextYear, month = birthday.month, day = birthday.day)
    else:
        birthdayLunar = sxtwl.fromSolar(birthday.year,birthday.month,birthday.day)
        nowTimeLunar = sxtwl.fromSolar(nowTime.year,nowTime.month,nowTime.day)
        nextYear = nowTimeLunar.getLunarYear()
        if nowTimeLunar.getLunarMonth() > birthdayLunar.getLunarMonth() :
            nextYear += 1
        elif  nowTimeLunar.getLunarMonth() == birthdayLunar.getLunarMonth() and nowTimeLunar.getLunarDay() > birthdayLunar.getLunarDay() :
            nextYear += 1
        elif nowTimeLunar.getLunarMonth() == birthdayLunar.getLunarMonth() and nowTimeLunar.isLunarLeap() and not birthdayLunar.isLunarLeap():
            nextYear += 1
        # 当年当月是闰月的算闰月生日 之后的闰月不算
        if nowTimeLunar.isLunarLeap() and nextYear == nowTimeLunar.getLunarYear() and birthdayLunar.getLunarYear() == nowTimeLunar.getLunarYear():
            nowBirthdayLunar = sxtwl.fromLunar(nextYear,birthdayLunar.getLunarMonth(),birthdayLunar.getLunarDay(),isRun=True)
        elif nowTimeLunar.isLunarLeap() and nextYear == nowTimeLunar.getLunarYear():
            nowBirthdayLunar = sxtwl.fromLunar(nextYear+1,birthdayLunar.getLunarMonth(),birthdayLunar.getLunarDay())
        else:
            nowBirthdayLunar = sxtwl.fromLunar(nextYear,birthdayLunar.getLunarMonth(),birthdayLunar.getLunarDay())
        # 生日为农历大月最后一天
        leap = birthdayLunar.getLunarDay() == 30 and nowBirthdayLunar.getLunarDay() != 30
        while leap:
            nextYear += 1
            nowBirthdayLunar = sxtwl.fromLunar(nextYear,birthdayLunar.getLunarMonth(),birthdayLunar.getLunarDay())
            leap = birthdayLunar.getLunarDay() == 30 and nowBirthdayLunar.getLunarDay() != 30
        return datetime(year = nowBirthdayLunar.getSolarYear(),month = nowBirthdayLunar.getSolarMonth(),day = nowBirthdayLunar.getSolarDay())

nowTime = datetime.today()

# 农历生日 09 19
birthday1 = datetime(year=2000, month=10, day=16)
chuxi_day = datetime(year=2023, month=1, day=21)

lunar1 = get_next_birthday(nowTime, birthday1, 2)
chuxi = get_next_birthday(nowTime, chuxi_day, 2)

lun_str = str(lunar1)
chuxi_str = str(chuxi)

# 生日日期
birth = _datetime.datetime(lunar1.year, lunar1.month, lunar1.day)
# 除夕日期
chuxi_days = _datetime.datetime(chuxi.year, chuxi.month, chuxi.day)

# 生日日期
d = birth - nowTime;
# 除夕日期
cx_d = chuxi_days - nowTime;

# 生日日期字符串化
str_days = str(d);
date_times = str_days.split(",")[1].split(":")

# 除夕日期字符串化
str_chuxi = str(cx_d);
data_chuxi = str_chuxi.split(",")[1].split(":")



today = datetime.now()
start_date = "2020-11-25"

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = "http://t.weather.itboy.net/api/weather/city/101280800"
  res = requests.get(url).json()
  detail_info = res['data']
  weather = res['data']['forecast'][0]
  return weather['type'], detail_info['wendu'], weather['low'], weather['high'], weather['aqi'], weather['fl'], weather['notice']

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

wea, wendu, low, high, aqi, fl, notice = get_weather();

# 1. 展示今日
def get_daliy_time_desc():
  return "今天是："+str(_datetime.datetime.now()).split(" ")[0]+ get_week_day(_datetime.datetime.now())+"<br/>";
# 2. 天气
def get_weather_desc_1():
  return " 今日天气："+wea+",当前温度:"+wendu+"<br/>";
def get_weather_desc_2():
  return " 最高温度："+high+",最低温度："+low+"<br/>";
def get_weather_desc_3():
  return " 风向等级："+fl+",今日空气质量："+str(aqi)+"<br/>";
def get_weather_desc_4():
  return " 小tips:" + notice +"<br/>";
# 3.生日统计
def get_birthday(d, date_times):
  return "距离生日小美女还有："+str(d.days)+"天"+str(date_times[0])+"小时"+str(date_times[1])+"分钟 <br/>";
# 4.除夕倒计时
def get_chuxi_days(cx_d, data_chuxi):
  return "距离除夕还有："+str(cx_d.days)+"天"+str(data_chuxi[0])+"小时"+str(data_chuxi[1])+"分钟 <br/>";
# 5.好吃推荐
def get_words():
  return "【红烧肉】【蒜香油麦菜】【爆炒午餐肉】【炝拌干豆腐丝】【鱼香肉丝】【番茄炒蛋】【茄子炒肉沫】【韭菜炒蛋】【酱烧豆腐】【排骨饭】<br/>"
# 6.周年函数
def get_cele_desc():
  return "已经在一起"+str(get_total_year())+"周年"+str(get_count())+"天哒,还有"+str(get_cele_date())+"天开启第"+str((get_total_year()+1))+"周年~";

client = WeChatClient(app_id, app_secret)
wm = WeChatMessage(client)
data = {"today":{"value":get_daliy_time_desc()},
"weather1":{"value":get_weather_desc_1()},
"weather2":{"value":get_weather_desc_2()},
"weather3":{"value":get_weather_desc_3()},
"weather4":{"value":get_weather_desc_4()},
"next_birthday":{"value":lun_str.split(" ")[0]},
"birthday": {"value":get_birthday(d,date_times)},
"newyear": {"value":get_chuxi_days(cx_d, data_chuxi)},
"next_year": {"value":chuxi_str.split(" ")[0]},
"words": {"value":get_words()},
"celeyear": {"value":get_cele_desc()}}



res = wm.send_template(user_id, template_id, data)
