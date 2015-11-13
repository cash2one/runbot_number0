#!/usr/bin/env python
# -*- coding:utf-8 -*-
#Copyright (C) 2013-2015 Runji
#
import roslib;  roslib.load_manifest('qbo_admin')
import rospy
import sys
from qbo_arduqbo.msg import BatteryLevel
from neo_talk.srv import Text2Speach

global client_speak
global battery_level

def speak_this(text):
    global client_speak
    client_speak(str(text))

def handle_topic(data):
    global battery_level
    level = data.level
    battery_level = data.level
    print "电池电源不足:%f"%level
    if level <13.0:
       speak_this("电池电量不足，请尽快连接外部电源")
       print "电源不足,告警"
    

def init_oam():
    global client_speak
    rospy.init_node('qbo_oam')
    client_speak = rospy.ServiceProxy("/say", Text2Speach)
    s = rospy.Subscriber("/battery_state", BatteryLevel, handle_topic)
    rospy.spin()

if __name__ == "__main__":
    init_oam()

