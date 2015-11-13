#!/usr/bin/env python
# -*- coding:utf-8 -*-
#Copyright (C) 2013-2015 Runji
#

import os
import time
import pyaudio
import audioop
import urllib2, pycurl
import base64
import json
import rospy
from qbo_speech_recognizer.msg import *

TOKEN_PATH = '/home/wang/.speech.token'

CROSS_NUM = 40
CH_NUM = 1
SAM_WID = 2
SAM_RAT = 16000
SEG_SIZE = SAM_RAT/4

recording = False
record_file = ''

access_token = None
publisher = None

def has_token():
    try:
        stat_info = os.stat(TOKEN_PATH)
    except OSError:
        return False
    if stat_info.st_size < 10: #invalid if too small
        return False
    db_ctime = stat_info.st_ctime
    create_date = time.strftime('%m', time.localtime(db_ctime))
    current_date = time.strftime('%m', time.localtime(time.time()))
    if current_date != create_date:
        return False   #old beyond 1 day, need update
    else:
        return True

def get_token():
    if has_token():
        fp = open(TOKEN_PATH, 'r')
        token = fp.readline().rstrip('\n')
        fp.close()
        return token
    apiKey = "FzXG8mmGoZBG0ytIVbMwY0SS"
    secretKey = "66a07f5adb56fedf0b7eeeb0845b882a"

    auth_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=" + apiKey + "&client_secret=" + secretKey;

    res = urllib2.urlopen(auth_url)
    json_data = res.read()
    token = json.loads(json_data)['access_token']
    fp = open(TOKEN_PATH, 'w')
    fp.write(token)
    fp.close()
    return token

def publish_topic(buf):
    #print 'curl return'
    json_data = json.loads(buf)
    err_msg = json_data['err_msg']
    if err_msg == 'success.':
        text = json_data['result'][0]  #baidu return a list of string
        publisher.publish(text.rstrip(u'，？'))#baidu add punctuation to every string
    else:
        rospy.loginfo('call cloud fail: %s' % err_msg)

def call_cloud(audio_data):
    global access_token
    f_len = len(audio_data)

    cuid = "acf7f3eda677" #my xiaomi phone MAC
    srv_url = 'http://vop.baidu.com/server_api' + '?cuid=' + cuid + '&token=' + access_token
    http_header = [
        'Content-Type: audio/pcm; rate=%d' % SAM_RAT,
        'Content-Length: %d' % f_len
    ]

    c = pycurl.Curl()
    c.setopt(pycurl.URL, str(srv_url)) #curl doesn't support unicode
    c.setopt(c.HTTPHEADER, http_header)   #must be list, not dict
    c.setopt(c.POST, 1)
    c.setopt(c.CONNECTTIMEOUT, 30)
    c.setopt(c.TIMEOUT, 30)
    c.setopt(c.WRITEFUNCTION, publish_topic)
    c.setopt(c.POSTFIELDS, audio_data)
    c.setopt(c.POSTFIELDSIZE, f_len)
    c.perform() #pycurl.perform() has no return val

def speech_recognize(str_data):
    global recording, record_file, access_token
    if audioop.cross(str_data, SAM_WID) > CROSS_NUM:
        if not recording:
            recording = True
            record_file = ''  #start a new record
        record_file = record_file + str_data
        #store audio data in record_file
    else:
        if recording:
            record_file = record_file + str_data
            #upload recorf file to cloud server and get result
            call_cloud(record_file)
            recording = False

if __name__ == '__main__':
    #get cloud API access token
    global access_token, publisher
    access_token = get_token()
    #open the input stream
    pa = pyaudio.PyAudio()
    stream = pa.open(format = pyaudio.paInt16, channels = CH_NUM,
                    rate = SAM_RAT, input = True,
                    frames_per_buffer = SEG_SIZE)
    #establish node
    publisher = rospy.Publisher('speech_text', SpeechText, queue_size=10)
    rospy.init_node('speech_recognizer', anonymous=True)
    print 'init success'

    while not rospy.is_shutdown():
        str_data = stream.read(SEG_SIZE)
        speech_recognize(str_data)


