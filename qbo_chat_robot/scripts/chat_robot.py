#!/usr/bin/env python
# -*- coding:utf-8 -*-
#Copyright (C) 2013-2015 Runji
#
import sys
import os
import roslib
import rospy
import urllib2
import json
from qbo_chat_robot.srv import *

NUM_ANS = 2

def proc_normal(json_msg):
    return json_msg['text']

def proc_surf(json_msg):
    answer = json_msg['text'] + u'，请看投影：'
    os.system('firefox ' + json_msg['url'] + ' &')
    return answer

def proc_news(json_msg):
    answer = json_msg['text'] + u'：'
    for item in json_msg['list'][0:NUM_ANS]:
        answer = answer + item['article'] + u'。'
    return answer

def proc_trains(json_msg):
    answer = json_msg['text'] + u'：'
    for item in json_msg['list'][0:NUM_ANS]:
        answer = answer + item['trainnum'] + u'，出发时间' + item['starttime'] + u'，到达时间' + item['endtime'] + u'。'
    return answer

def proc_airline(json_msg):
    answer = json_msg['text'] + u'：'
    for item in json_msg['list'][0:NUM_ANS]:
        answer = answer + item['flight'] + u'，出发时间' + item['starttime'] + u'，到达时间' + item['endtime'] + u'。'
    return answer

def proc_cook(json_msg):
    answer = json_msg['text'] + u'：'
    for item in json_msg['list'][0:NUM_ANS]:
        answer = answer + item['name'] + u'，用料：%s；调料：%s。' % tuple(item['info'].split(' | '))
    return answer

tbl_msg_op = {'100000':proc_normal, '200000':proc_surf, '302000':proc_news, '305000':proc_trains, '306000':proc_airline, '308000':proc_cook}

def handle_question(req):
    html = urllib2.urlopen(r'http://www.tuling123.com/openapi/api?key=7e310962d12a8b782dec54474ffc6b25&info='+req.question + r'&loc=' + '西安市')

    hjson = json.loads(html.read())
    category = hjson['code']
    category = str(category) #hjson['code'] return int, not string, so need conversion for tbl[key]
    try:
        proc_fun = tbl_msg_op[category]
        answer = proc_fun(hjson)
        answer = answer.split(u'。')[0]
    except KeyError:
        answer = u'我被你问住了！' + json.dumps(hjson)
    return ChatRobotResponse(answer)



if __name__ == "__main__":
    rospy.init_node('qbo_chat_robot')

    #start robot
    s0 = rospy.Service('/qbo_chat_robot', ChatRobot, handle_question)

    rospy.spin()

