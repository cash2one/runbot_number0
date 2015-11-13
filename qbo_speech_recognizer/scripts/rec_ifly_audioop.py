#!/usr/bin/env python
# -*- coding:utf-8 -*-
#Copyright (C) 2013-2015 Runji
#

import pyaudio
import wave
import subprocess
import audioop
import rospy
from qbo_speech_recognizer.msg import *

TEMP_REC_FILE = '/home/wang/projects/speech/x.wav'
TEMP_LOG_FILE = '/home/wang/projects/speech/log_ifly.log'

#need 2 arg, arg1 = sample rate:8/16, arg2 = wav file path
IFLY_IAT_FILE = '/home/wang/packages/KeDaXunFei/bin/iatdemo' #put libmsc.so to /usr/lib

CROSS_NUM = 40
CH_NUM = 1
SAM_WID = 2
SAM_RAT = 16000
SEG_SIZE = SAM_RAT/2

recording = False
record_file = None

access_token = None
publisher = None


def call_cloud():
    left_margin = 'The result is: '
    result = ''
    logf = open(TEMP_LOG_FILE, 'w')
    subprocess.call([IFLY_IAT_FILE, '%s'%(SAM_RAT/1000), TEMP_REC_FILE], stdout=logf)
    logf = open(TEMP_LOG_FILE, 'r')
    for line in logf:
        if line.startswith(left_margin):
            result = line.lstrip(left_margin).rstrip()
            break
    logf.close()
    if result != '':
        publisher.publish(result)
    else:
        rospy.loginfo('call cloud fail')

def speech_recognize(str_data):
    global recording, record_file
    if audioop.cross(str_data, SAM_WID) > CROSS_NUM:
        if not recording:
            recording = True
            record_file = wave.open(TEMP_REC_FILE, 'wb')
            record_file.setnchannels(CH_NUM)
            record_file.setsampwidth(SAM_WID)
            record_file.setframerate(SAM_RAT)
        record_file.writeframes(str_data)
        #store audio data in record_file
    else:
        if recording:
            record_file.writeframes(str_data)
            record_file.close()
            recording = False
            #upload record file to cloud server and get result
            call_cloud()

if __name__ == '__main__':
    global publisher
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


