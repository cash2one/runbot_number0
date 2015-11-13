#!/usr/bin/env python
#-*- coding:utf-8 -*-
#Copyright (C) 2012-2013 Thecorpora Inc.
#
#This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.
#
#This program is distributed in the hope that it will be useful,but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

import rospy
import os
import subprocess
from questions import *
from qbo_smart_home_services.srv import *

def smarthomefenci(sentence,language):
    seg_list=[]
    seg_list1=jieba.cut(sentence)
    for seg in seg_list1:
        seg_list.append(seg)
    for location in location_list:
	if location in seg_list:
           param_location = location
           print param_location
	   for device in device_list:
		if device in seg_list:
                   param_device = device
    		   print param_device
		   for action in action_list:
		       if action in seg_list:
           	          param_action = action
                          print param_action
    if param_location!="" and param_device!="" and param_action!="":
       print "param OK"

def smarthomectrl(sentence,language):
    # call "/say" service to speak selected words
    rospy.wait_for_service("/smart_home_set_host")
    client_sethost = rospy.ServiceProxy("/smart_home_set_host", SetHost)
    rospy.wait_for_service("/smart_home_single_ctrl")
    client_singlectrl = rospy.ServiceProxy("/smart_home_single_ctrl", SingleCtrl)
#    print "sentence:%s"%sentence
#    print "language:%s"%language
#    sentencelist=sentence.split(' ',2)
#    print sentencelist[1]
#    txtname=sentencelist[1]
    smarthomefenci(sentence,language)
    client_sethost("192.168.0.134")
#    client_singlectrl("客厅", "吊灯左", "开") 
    client_singlectrl(param_location, param_device, param_action) 
#    client_speak("客厅吊灯开")
 
#    rospy.wait_for_service("/qbo_face_recognition/train");
#    service_facetrain = rospy.ServiceProxy('/qbo_face_recognition/train', Train)
#    res = service_facetrain()
#    rospy.loginfo(res.taught)
#    return "你好%s,我已经认识你了"%personname
