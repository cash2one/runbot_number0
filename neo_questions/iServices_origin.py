#!/usr/bin/env python
#-*- coding:utf-8 -*-
#-*- coding:utf-8 -*-
#Copyright (C) 2012-2013 Thecorpora Inc.
#
#This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.
#
#This program is distributed in the hope that it will be useful,but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

import rospy
import json
from qbo_internet_services.srv import InternetService
import sys
import string

def read_weather_dic():
    global date_list
    global city_list


    date_list=[]
    city_list=[]
    path = roslib.packages.get_pkg_dir("neo_questions")
    with open(path+'/weatherdata/date.dic') as fp:
        print "date list:"
        for line in fp:
            date = line.rstrip('\n')
            print date
            print "next:"
            location_list.append(date.decode('utf-8'))
    with open(path+'/weatherdata/city.dic') as fp:
        print "city list:"
        for line in fp:
            city = line.rstrip('\n')
            print city
            print "next:"
            city_list.append(city.decode('utf-8'))
def location(sentence,language):
    reload(sys)
    sys.setdefaultencoding('utf8')
    rospy.wait_for_service("/internetservices");
    service_iservices = rospy.ServiceProxy('/internetservices', InternetService)
    info = service_iservices("location","")
    decodedData=json.loads(info.info)
    if type(decodedData) is dict:
        city=decodedData['city']
        country=decodedData['country']
    else:
        print "Not valid JSON recived"
    response="我们位于"+country+","+city+"市"
#    response="我们位于"+country+","+city
#    response="We are in "+city+", in "+country
    rospy.loginfo(response)
    return response
def weather_fenci(sentence,language):
    global date_list
    global city_list
    global param_date
    global param_city
  
    sentence=sentence.decode('utf8')
    seg_list=[]
    print sentence.replace(" ","")
    seg_list1=jieba.cut(sentence.replace(" ",""))
    for seg in seg_list1:
        seg_list.append(seg)
        print seg
    for date in date_list:
        if sentence.find(date) > -1:
           param_date = date
           print "date:%s matched!"%param_date
           break
        else:
           print "date:%s not matched!"%date
           param_date= "" 
    for city in city_list:
        if sentence.find(city) > -1:
           param_city = city
           print "city:%s matched!"%param_city
           break
        else:
           print "city:%s not matched!"%city
           param_city= ""
    return True

def weather(sentence,language):
    reload(sys)
    sys.setdefaultencoding('utf8')
    weather_fenci(sentence,language)
    
    rospy.wait_for_service("/internetservices");
    service_iservices = rospy.ServiceProxy('/internetservices', InternetService)
    info = service_iservices("weather", param_date, param_city)
    decodedData=json.loads(info.info)
    if type(decodedData) is dict:
        stemp=decodedData['temp']
        print "temperature:%s"%stemp
        temp=string.atof(stemp)
# Convert to celsius(comment farenheit conversion if you uncomment this line):
        print "temperature:%f"%temp
        temp=(temp-32)*5/9

# Convert to Farenheit (comment celsius conversion if you uncomment this line)
#        temp=((temp*9)/5)-459.67
        if temp-int(temp)>=0.5:
            temp=int(temp)+1
        else:
            temp=int(temp)
        desc=decodedData['description']
    else:
        print "Not valid JSON recived"
    response="%s %s天气:"+desc+",温度"+str(temp) +" 摄氏度"(%param_date, %param_city)
#    response="Today is "+desc+" and the temperature is of "+str(temp) +" degrees"
    rospy.loginfo(response)
    return response

