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
import time

from neo_talk.srv import *

robot_name=u'润基豆豆'
def voicegetselfname(sentence,language):
    global robot_name
    return "你好,我是%s"%robot_name
def voicelearnname(sentence,language):
    global robot_name
    # call "/say" service to speak selected words
#    client_speak = rospy.ServiceProxy("/say", Text2Speach)
    print "sentence:%s"%sentence
    print "language:%s"%language
    sentencelist=sentence.split(' ',2)
    print sentencelist[1]
    robot_name=sentencelist[1]
 #   client_speak("好的,我记住了,我是%s"%personname)
    return "好的,我记住了,我是%s"%robot_name
