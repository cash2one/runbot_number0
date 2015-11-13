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

from neo_talk.srv import *

def readtxt(sentence,language):
    # call "/say" service to speak selected words
    client_speak = rospy.ServiceProxy("/say", Text2Speach)
    print "sentence:%s"%sentence
    print "language:%s"%language
    sentencelist=sentence.split(' ',2)
    print sentencelist[1]
    txtname=sentencelist[1]
    client_speak("现在开始背诵%s"%txtname)
    client_speak("-f /home/runji/%s.txt"%txtname)
 
#    rospy.wait_for_service("/qbo_face_recognition/train");
#    service_facetrain = rospy.ServiceProxy('/qbo_face_recognition/train', Train)
#    res = service_facetrain()
#    rospy.loginfo(res.taught)
#    return "你好%s,我已经认识你了"%personname
def playwav(sentence,language):
    # call "/say" service to speak selected words
    client_speak = rospy.ServiceProxy("/say", Text2Speach)
    print "sentence:%s"%sentence
    print "language:%s"%language
    sentencelist=sentence.split(' ',2)
    print sentencelist[1]
    wavname=sentencelist[1]
    wavfile="/home/runji/%s.wav"%wavname
    client_speak("现在开始播放%s"%wavname)
    os.system("aplay /home/runji/%s.wav"%wavname)
    os.system("mplayer /home/runji/%s.mp3"%wavname)
#    subprocess.call(['aplay', wavfile])
