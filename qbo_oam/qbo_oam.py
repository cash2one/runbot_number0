#!/usr/bin/env python
# -*- coding:utf-8 -*-
#Copyright (C) 2013-2015 Runji
#
import roslib;  roslib.load_manifest('qbo_admin')
import rospy
import sys
from qbo_arduqbo.msg import BatteryLevel
from neo_talk.srv import Text2Speach
#battery_level = 1.0
global client_speak

globalvarpath = roslib.packages.get_pkg_dir("qbo_globalvar")
sys.path.append(globalvarpath)

import qbo_globalvar as GlobalVar
#battery_level = 0.0
def speak_this(text):
    global client_speak
    client_speak(str(text))

def handle_topic(data):
#    global battery_level
    level = data.level
#    qbo_globalvar.battery_level = data.level
    GlobalVar.set_battery(data.level)
    print "电池电源不足:%f"%GlobalVar.get_battery()#level
    if level <8.0:
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

