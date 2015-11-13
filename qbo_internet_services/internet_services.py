#!/usr/bin/env python
# -*- coding:utf-8 -*-
#Copyright (C) 2013-2015 Runji
#
import sys
import roslib
import rospy
from qbo_internet_services.srv import *

import json
import urllib2

def geoip_Location():
    weatherJson = urllib2.urlopen(r'https://api.thinkpage.cn/v2/weather/now.json?city=ip&language=zh-chs&unit=c&key=6U0O4HUCQ4')
    decodedW = json.loads(weatherJson.read())    
    city = decodedW['weather'][0]['city_name']
    formated_loc=json.dumps({"city":city,"country":u'中国',"countryAb":'CHN',"latitude":12.34,"longitude":56.78})
    return formated_loc

def weather(date, coordinates):
    if coordinates=="":
        coordinates = 'ip'
    else:
        coordinates = coordinates.encode('utf-8')

    weatherJson = urllib2.urlopen(r'https://api.thinkpage.cn/v2/weather/all.json?city='+coordinates+'&language=zh-chs&unit=c&key=6U0O4HUCQ4')
    decodedW = json.loads(weatherJson.read())
    if "OK" == decodedW['status']:
        city_name = decodedW['weather'][0]['city_name']
        weather_data = decodedW['weather'][0]['future']
        time_index = 0
        time_name = u'今天'
        if date == '' or date == u'今天':
            time_index = 0
            time_name = u'今天'
        elif date == u'明天':
            time_index = 1
            time_name = u'明天'
        else:
            print 'unsupport date!'
        temp_min = weather_data[time_index]['low']
        temp_max = weather_data[time_index]['high']
        description = weather_data[time_index]['text'].replace('/', u'转')
        wind_deg = weather_data[time_index]['wind']
        #response = city_name + time_name + description + u'，' + wind_deg + u'，' + u'最高温度' + temp_max+ u'摄氏度，' + u'最低温度' + temp_min + u'摄氏度'
        response = u'%s%s%s，%s，最高温度%s摄氏度，最低温度%s摄氏度'%(city_name, time_name, description, wind_deg, temp_max, temp_min)
        return response
    else:
        print 'unkown city!'
        return "-1"

def handle_service(req):
    print "Service called:"+req.service
    if req.service=="location":
        resp = geoip_Location()
        return InternetServiceResponse(resp)
    elif req.service=="weather":
        resp = weather(req.date.decode('utf-8') , req.city.decode('utf-8') )
        return InternetServiceResponse(resp)
    else:
        print "Service doesn't exist"
        response="-1"
        return InternetServiceResponse(response)

def init_server():
    rospy.init_node('Internet_Services')
    s = rospy.Service('/internetservices', InternetService, handle_service)
    rospy.spin()

if __name__ == "__main__":
    init_server()

