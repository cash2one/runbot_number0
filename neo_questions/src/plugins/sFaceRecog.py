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

from qbo_face_msgs.srv import GetName
from qbo_face_msgs.srv import LearnFaces
from qbo_face_msgs.srv import Train
from qbo_face_msgs.srv import RecognizeFace
from neo_talk.srv import *

def test(sentence,language):
    print "sentence:%s"%sentence
    print "language:%s"%language
#    rospy.loginfo(res.name)
#    rospy.loginfo(res.recognized)
#    return res.name
def facerecog(sentence,language):
    print "sentence:%s"%sentence
    print "language:%s"%language
    rospy.wait_for_service("/qbo_face_recognition/recognize_with_stabilizer");
    service_pluginfacerecog = rospy.ServiceProxy('/qbo_face_recognition/recognize_with_stabilizer', RecognizeFace)
    res = service_pluginfacerecog()
    rospy.loginfo(res.name)
    rospy.loginfo(res.recognized)
    if res.recognized == True:
        return "你好%s"%res.name
    else:
        return "亲不好意思，我暂时还不认识你呢"

def facegetname(sentence,language):
    os.system("rosparam set /qbo_face_tracking/send_to_recognizer true")
    time.sleep(0.5)
    print "sentence:%s"%sentence
    print "language:%s"%language
    rospy.wait_for_service("/qbo_face_recognition/get_name");
    service_pluginfacegetname = rospy.ServiceProxy('/qbo_face_recognition/get_name', GetName)
    res = service_pluginfacegetname()
    rospy.loginfo(res.name)
    rospy.loginfo(res.recognized)
    os.system("rosparam set /qbo_face_tracking/send_to_recognizer false")
    if res.recognized == False:
        return "人脸识别失败"
    elif res.recognized == True and res.name == "":
        return "亲,不好意思，我还不认识你呢"
    else:
        return "你好,你是%s"%res.name
def facelearnname(sentence,language):
    # call "/say" service to speak selected words
    client_speak = rospy.ServiceProxy("/say", Text2Speach)
    print "sentence:%s"%sentence
    print "language:%s"%language
    sentencelist=sentence.split(' ',4)
    print sentencelist[3]
    personname=sentencelist[3]
    client_speak("你好%s,稍等, 不要离开，让我认识一下你"%personname)
    rospy.wait_for_service("/qbo_face_recognition/learn_faces");
    service_facelearnname = rospy.ServiceProxy('/qbo_face_recognition/learn_faces', LearnFaces)
    res = service_facelearnname(personname)
    rospy.loginfo(res.learned)
 
    rospy.wait_for_service("/qbo_face_recognition/train");
    service_facetrain = rospy.ServiceProxy('/qbo_face_recognition/train', Train)
    res = service_facetrain()
    rospy.loginfo(res.taught)
    return "你好%s,我已经认识你了"%personname
