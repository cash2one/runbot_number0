#!/usr/bin/env python
# -*- coding:utf-8 -*-
#Copyright (C) 2013-2015 Runji
#
import roslib;  roslib.load_manifest('qbo_globalvar')
import rospy
import sys

battery_level=[0.0,1]
class GlobalVar: 
      battery_level=[0.0,1]
#      battery_level[0] = 0.0
#      def set_battery(self,x):
#          self.battery_level=x
#      def get_battery(self):
#          return self.battery_level
def set_battery(x):
    GlobalVar.battery_level[0]=x
def get_battery():
    return GlobalVar.battery_level[0]
       
