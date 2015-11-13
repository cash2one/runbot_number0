#!/usr/bin/env python
# -*- coding:utf-8 -*-
#Copyright (C) 2013-2015 Runji
#

import pyaudio
import wave
import subprocess
import audioop
import rospy
from std_msgs.msg import String

TEMP_REC_FILE = '/tmp/s.wav'
TEMP_LOG_FILE = '/tmp/s.log'
NOISE_PROFILE = '/tmp/noise.profile'

#need 2 arg, arg1 = sample rate:8/16, arg2 = wav file path
IFLY_IAT_FILE = '/usr/bin/iatdemo' #put libmsc.so to /usr/lib

CROSS_NUM = 40
CH_NUM = 1
SAM_WID = 2
SAM_RAT = 16000
SEG_SIZE = SAM_RAT/4

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


if __name__ == '__main__':
    global publisher
    #generate noise profile
    null_file = open('/dev/null', 'w')
    subprocess.call(['rec', '-r', '%s'%SAM_RAT, '-c', '%s'%CH_NUM, '-n', 'trim', '0.5', '1.5', 'noiseprof', NOISE_PROFILE], stdout=null_file)
    #establish node
    rospy.init_node('recognizer')
    publisher = rospy.Publisher('~output', String)
    print 'init success'

    while not rospy.is_shutdown():
        #record a sentence to temp file
        subprocess.call(['rec', '-r', '%s'%SAM_RAT, '-c', '%s'%CH_NUM, TEMP_REC_FILE, 'noisered', NOISE_PROFILE, 'silence', '1', '0.2', '2%', '1', '0.2', '2%', 'norm'], stderr=null_file)
        #upload temp file to cloud service, and get result
        call_cloud()

