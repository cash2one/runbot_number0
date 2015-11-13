#!/usr/bin/env python
#-*- coding: utf-8 -*-
#Copyright (C) 2012-2013 Thecorpora Inc.
#
#This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.
#
#This program is distributed in the hope that it will be useful,but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
#  Modified by Vincent FOUCAULT elpimous12@orange.fr
#
#  for pocketsphinx use, in replacement of julius (julius issues on ubuntu > electric version)
#
#####################################################################################

import roslib;roslib.load_manifest('neo_questions')
import rospy
from neo_talk.srv import *
from iServices import *
from qbo_face_msgs.msg import FacePosAndDist
from std_msgs.msg import String
from qbo_smart_home_services.srv import *
from qbo_chat_robot.srv import *
from qbo_arduqbo.srv import BatteryQuery
import random
import sys
import os 
import jieba
import sqlite3
import subprocess
from subprocess import Popen, PIPE, STDOUT

#Load plugins directory
path = roslib.packages.get_pkg_dir("neo_questions")
globalvarpath = roslib.packages.get_pkg_dir("qbo_globalvar")
sys.path.append(path+"/src/plugins")
sys.path.append(globalvarpath)
global client_speak
global face_detected
global dialogue
global subscribe
global plugins
global lang
global device_last
global location_last
global keywords_to_context
global client_batteryquery
global last_sentence
import qbo_globalvar as GlobalVar
#global battery_level

device_last="吊灯"
location_last="客厅"
ROBOT_ID="00000000".decode('utf-8')
ROBOT_NAME="豆豆".decode('utf-8')
ROBOT_YEAR="我刚刚两岁啦".decode('utf-8')
ROBOT_PARENT="我的爸爸妈妈是一群聪明的工程师".decode('utf-8')
ROBOT_SEX="我是美女吆".decode('utf-8')
ROBOT_HOMETOWN="我来字西安,智库信息科技有限公司".decode('utf-8')
ROBOT_HOBBY="我会唱歌,背古诗,讲故事,能够安全巡逻,能够家居控制,播报天气预报等,还有许多新功能正在学习中".decode('utf-8')
PERSONINFO_DEFAULT=[ROBOT_ID, ROBOT_NAME, ROBOT_YEAR, ROBOT_SEX, ROBOT_PARENT, ROBOT_HOMETOWN, ROBOT_HOBBY]

DB_FILE = 'personinfo.db'
db_conn = None
report_file = None


def system_language(data):
    try:
        set_language(data.data)
        rospy.loginfo("Language changed to "+data.data)
    except KeyError:
        rospy.loginfo("Error: Language not recognized("+data.data+")")

def getbattery(sentence, lang):
#    global battery_level
    res = GlobalVar.get_battery()

    print"现在电池电压为%f伏"%res
    return "现在电池电压为%f伏"%res
def speak_this(text):
    global client_speak
    client_speak(str(text))
def smarthomefenci(sentence,language):
    global location_list
    global device_list
    global action_list
    global param_location
    global param_device
    global param_action
    global device_last
    global location_last
  
    sentence=sentence.decode('utf8')
    seg_list=[]
    print sentence.replace(" ","")
    seg_list1=jieba.cut(sentence.replace(" ",""))
    for seg in seg_list1:
        seg_list.append(seg)
        print seg
    for action in action_list:
        if sentence.find(action) > -1:
           param_action = action
           print "action:%s matched!"%param_action
           for device in device_list:
               if sentence.find(device) > -1:
                  param_device = device
                  device_last = device
                  print "device:%s matched!"%param_device
	          for location in location_list:
                      if sentence.find(location) > -1:
                         param_location = location
                         location_last= location
    		         print "location:%s matched!"%param_location
                         return True
                      else:
                         print "location:%s not matched!"%location
                  param_location= location_last #u"客厅"
                  print "default location:%s assumped!"%param_location
                  return True
	       else:
                  print "device:%s not matched!"%device
           param_device= device_last  
           param_location= location_last
           print "default location:%s and device:%s assumped!"%(param_location,param_device)
           return True
        else:
           print "action:%s not matched!"%action

#    if (param_location != "") and (param_device != "") and (param_action != ""):
#       print "param OK"
#       return True
#    else: 
    return False

def chat_robot(sentence,language):
    rospy.wait_for_service("qbo_chat_robot")
    client_chat = rospy.ServiceProxy("qbo_chat_robot", ChatRobot)
    response  = client_chat(sentence)
    text = response.answer
    print text
    speak_this(text)
def smarthomectrl(sentence,language):
    global location_list
    global device_list
    global action_list
    global param_location
    global param_device
    global param_action
    if (smarthomefenci(sentence,language) != True):
        print "smarthome command not recognized!"
        return False 
    print "smarthome command recognized ok!"
    #rospy.wait_for_service("/smart_home_set_host")
    #client_sethost = rospy.ServiceProxy("/smart_home_set_host", SetHost)
    rospy.wait_for_service("/smart_home_single_ctrl")
    client_singlectrl = rospy.ServiceProxy("/smart_home_single_ctrl", SingleCtrl)
#    print "sentence:%s"%sentence
#    print "language:%s"%language
#    sentencelist=sentence.split(' ',2)
#    print sentencelist[1]
#    txtname=sentencelist[1]
#    print "smarthome ip:%s"%(client_sethost("192.168.0.109"))
#    client_singlectrl("客厅", "吊灯左", "开") 
    if (client_singlectrl(param_location, param_device, param_action) == True):
       print "smarthome ctrl success"
       return True
    else:
       print "smarthome ctrl failed"
       return False
def get_context(data):
    global keywords_to_context
    for(context, keywords) in keywords_to_context.iteritems():
        for word in keywords:
           if data.find(word) > -1:
              return context
def personinfo(sentence,lang):
    data = sentence
    
#    if(data.find("名字") > -1):
#        text = ROBOT_NAME
#    if((data.find("年龄") > -1) or (data.find("几岁") > -1) or (data.find("多大") > -1)):
#        text = ROBOT_YEAR
    if((data.find("美女") > -1) or (data.find("帅哥") > -1) or (data.find("男孩") > -1) or (data.find("女孩") > -1)):
        text = ROBOT_SEX
    elif(data.find("家乡") > -1):
        text = ROBOT_HOMETOWN
    elif((data.find("爸爸") > -1) or (data.find("妈妈") > -1)):
        text = ROBOT_PARENT
    elif((data.find("特长") > -1) or (data.find("自我介绍") > -1)):
        text = ROBOT_HOBBY
    print text
    return text
def getJiujintai(sentence, lang):
    global keywords_to_context
    key_list=keywords_to_context["jiujintai"]
    for keyword in key_list:
        txtname=keyword
        if sentence.find(keyword) > -1:
           txtfile="/opt/ros/hydro/catkin_ws/src/OpenQbo/neo_questions/jiujintai/%s.txt"%txtname
           wavfile="/opt/ros/hydro/catkin_ws/src/OpenQbo/neo_questions/jiujintai/%s.txt.wav"%txtname
#           client_speak("九锦台的%s是这样的:"%txtname)
           if os.path.isfile(wavfile):
               os.system("aplay %s"%wavfile)
               print "%s already exist!!"
           else:
#           client_speak("-f ../jiujintai/%s.txt"%txtname)
               client_speak("-f %s"%txtfile)
           return True
    return False 
def mediaplay(sentence,language):
    mediaplay_list=["播放","唱"]
    mediawav_list=["小苹果","沙沙沙"]
  
    sentence=sentence.decode('utf8')
    seg_list=[]
    print sentence.replace(" ","")
    for play in mediaplay_list:
        if sentence.find(play) > -1:
           for wavname in mediawav_list:
               if sentence.find(wavname) > -1:
                      wavfile="/home/runji/%s.wav"%wavname
                      client_speak("现在开始播放%s"%wavname)
                      os.system("aplay /home/runji/%s.wav"%wavname)
                      os.system("mplayer /home/runji/%s.mp3"%wavname)
                      return True
	       else:
                  print "wavfile:%s not in wavlist!"%wavname
           wavname ="小苹果"
           print "default wavname:%s assumped!"%wavname
           client_speak("我会唱歌啊,下面先唱一首%s,欢迎点歌"%wavname)
           os.system("aplay /home/runji/%s.wav"%wavname)
           return True
        else:
           print "play action:%s not matched!"%play
    return False
def educationread(sentence,language):
    txtread_list=["朗诵","背诵","朗读","阅读","背唐诗","背古诗"]
    txtname_list=["静夜思","悯农"]
  
    sentence=sentence.decode('utf8')
    seg_list=[]
    print sentence.replace(" ","")
    for txtread in txtread_list:
        if sentence.find(txtread) > -1:
           for txtname in txtname_list:
               if sentence.find(txtname) > -1:
                      txtfile="/home/runji/%s.wav"%txtname
                      client_speak("现在开始背诵%s"%txtname)
                      client_speak("-f /home/runji/%s.txt"%txtname)
                      return True
	       else:
                  print "txtfile:%s not in wavlist!"%txtname
           txtname ="静夜思"
           print "default txtname:%s assumped!"%txtname
           client_speak("好的,我来背诵%s"%txtname)
           client_speak("-f /home/runji/%s.txt"%txtname)
           return True
        else:
           print "read action:%s not matched!"%txtread
#           client_speak("下面我来背诵%s"%txtname)
#           client_speak("-f /home/runji/%s.txt"%txtname)
    return False
def launchVoiceNavNode():
    rospy.loginfo("Qbo questions: Launching voice navigation nodes")
    cmd = "rosrun rbx1_speech voice_nav.py"
    subprocess.Popen(cmd.split())
    rospy.loginfo(" END Launching voice navigation nodes")
def stopVoiceNavNode():
        try:
            rospy.loginfo("Qbo Question: Killing Voice navigation nodes")
            #self.processFaceNode.send_signal(signal.SIGTERM)
            cmd="rosnode kill /voice_nav"
            subprocess.Popen(cmd.split())
        except Exception as e:
            rospy.loginfo("ERROR when trying to kill Voice navigation Process. The process may not exist: "+str(e))
        rospy.loginfo(" END Stopping Voice navigation Nodes")
        return "ok"
def modeselect(sentence, lang):
    data = sentence
    if(data.find("开启运动模式") > -1):
        launchVoiceNavNode()
        text = "成功开启运动模式"
    elif(data.find("关闭运动模式") > -1):
        stopVoiceNavNode()
        text = "成功关闭运动模式"
    print text   
def getVoiceType(sentence, lang):
#    voice_list=["陕西话","河南话","普通话","广东话"]
#    sentence_=sentence.decode('utf8')
    data = sentence
    if(data.find("陕西话") > -1):
        text = "shannxihua"
    elif(data.find("河南话") > -1):
        text = "henanhua"
    elif(data.find("普通话") > -1):
        text = "mandrian"
    elif((data.find("四川话") > -1)):
        text = "sichuanhua"
    elif((data.find("广东话") > -1) or (data.find("粤语"))):
        text = "yueyu"
    print text
    return text
def setVoiceType(voice):
    rospy.wait_for_service("/set_voicetype")
    client_set_voicetype = rospy.ServiceProxy("/set_voicetype", SetVoice)
    client_set_voicetype(voice)
def listen_callback(msg):
    global face_detected  
    global dialogue
    global keywords_to_context
    global last_sentence 
    text=""
    sentence = msg.data
    sentence=sentence.upper()
#    sentence=sentence.replace(" ","")
    rospy.loginfo("Listened: |"+sentence+"|")
    if sentence  == last_sentence:
        print "sentence repeated!!!"
        return 
    last_sentence  = sentence

    context = get_context(sentence)
    print context
#    print keywords_to_context[context]
#    for(context, keywords) in keywords_to_context.iteritems():
#        for word in keywords:
#           if data.find(word) > -1:
#              return context
 
    rospy.loginfo("Context:" + str(context))
 
    if context == 'jiujintai':
         getJiujintai(sentence, lang)
         return 
    elif context == 'smarthome':
         print context
#         smarthomectrl(sentence, lang)
#    elif context == 'motionctl':
    elif context == 'weather':
#         weather_fenci(sentence, lang)
         sentence=sentence.replace(" ","")
         text = weather(sentence,lang)
         speak_this(text)
         return 
    elif context == 'personinfo':
         text = personinfo(sentence,lang)
         speak_this(text)
         return 
    elif context == 'media':
         text = mediaplay(sentence,lang)
         return
#         print "media"
    elif context == 'education':
         text = educationread(sentence, lang)
         return 
    elif context == 'batteryquery':
         text = getbattery(sentence, lang)
         speak_this(text)
         return
    elif context == 'switch_voicetype':
#         text ="我会说" 
         voicetype = getVoiceType(sentence, lang)
         setVoiceType(voicetype)
         speak_this("很高兴见到你")
         print "已经准备好了"
         return
    elif context == 'modeselect':
         modeselect(sentence, lang)
         return  
    for i in range(12,1,-1):   
    	sentencecut=sentence.decode('utf8')[0:i].encode('utf8')
    	print "sentencecut:%s"%sentencecut
    	if sentencecut in dialogue:
            output = dialogue[sentencecut]
            choice=random.choice(output)
            if choice[0]=="$":
                choice=choice.replace("$","")
                choice=choice.lower()
                for plug in plugins:
                    try:
                       text=getattr(plug,choice)(sentence,lang)
                       print "text:%s"%(text)
                       speak_this(text)
	               return
                    except AttributeError:
                       rospy.loginfo("Attibute "+choice +" could not be found:"+ str(dir(plug)))
            else:
                text=choice
                speak_this(text)
                print text
	        return #break
        else:
            continue
#    print "begin to smarthomectrl:%s"%sentence
#    if(smarthomectrl(sentence, lang) == True):
#        return 
#    chat_robot(sentence, lang)

def face_callback(data):
    global face_detected
    face_detected = data.face_detected	

def read_smarthome_dic():
    global location_list
    global device_list
    global action_list
#    global device_last=u"吊灯"
#    global location_last=u"客厅"


    location_list=[]
    device_list=[]
    action_list=[]
    path = roslib.packages.get_pkg_dir("neo_questions")
    with open(path+'/smarthomedata/location.dic') as fp:
        print "location list:"
        for line in fp:
            location = line.rstrip('\n')
            print location
            print "next:"
            location_list.append(location.decode('utf-8'))
    with open(path+'/smarthomedata/device.dic') as fp:
        print "device list:"
        for line in fp:
            device = line.rstrip('\n')
            print device
            print "next:"
            device_list.append(device.decode('utf-8'))
    with open(path+'/smarthomedata/action.dic') as fp:
        print "action list:"
        for line in fp:
            action = line.rstrip('\n')
            print action
            print "next:"
            action_list.append(action.decode('utf-8'))
    
def read_dialogues(filename):
    global dialogue
    dialogue = {}

    f = open(filename)    
    for line in f.readlines():
        try:
            line = line.replace("\n","") 
            parts = line.split(">>>")

            dialogue_input = parts[0].strip()
            dialogue_output = parts[1].strip()
        
            # we check wheter the input line alreayd exists, if so, we add to its own list
            if dialogue_input in dialogue:                
                dialogue[dialogue_input].append(dialogue_output)
            else:
                #dialogue_input does not exist
                dialogue[dialogue_input] = [dialogue_output]
        except Exception:
            pass        

    f.close()

def set_language(lang):

    if lang!="es" and lang!="en":
       lang="cn"

    global subscribe
    try:
        subscribe.unregister()
        rospy.loginfo("Unregistered from previous language")
    except NameError:
        rospy.loginfo("First language set")


    path = roslib.packages.get_pkg_dir("neo_questions")
    filename = path+'/config/dialogues_'+lang
    print "Dialogue filename loaded: "+filename
    read_dialogues(filename)
    subscribe=rospy.Subscriber('recognizer/output', String, listen_callback)

def loadPlugins():
    global plugins
    plugins=[]
    path = roslib.packages.get_pkg_dir("neo_questions")
    for f in os.listdir(path+"/src/plugins/"):
        moduleName, ext = os.path.splitext(f) 
        if ext == '.py' and moduleName!="__init__":
            plugins.append(__import__(moduleName))

def initDB(base_dir):
    global db_conn
    db_path = os.path.join(base_dir, DB_FILE)
    db_conn = sqlite3.connect(db_path)
    c = db_conn.cursor()
    c.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="personinfo";')
    if c.fetchall() == []:
        c.execute('create table personinfo(robot_id text primary key not null, Name text, Year text, Sex text, Parent text, hometown text, hobby text);')
        db_conn.commit()

def IsinDB(robot_id):
    global db_conn
    c = db_conn.cursor()
    c.execute('select * from personinfo where robot_id = ?;', [robot_id])
    return 1 == len(c.fetchall())
def GetName(robot_id):
    global db_conn
    c = db_conn.cursor()
    for row in c.execute('select * from personinfo where robot_id = ?;', [robot_id]):
        if -1 != row[0].find(robot_id):
            print "GetName:%s"%row[1]
            return row[1]
def SetName(robot_id):
    global db_conn
    c = db_conn.cursor()
    for row in c.execute('select * from personinfo where robot_id = ?;', [robot_id]):
        if -1 != row[0].find(robot_id):
            print "GetName:%s"%row[1]
            return row[1]
def GetYear(robot_id):
    global db_conn
    c = db_conn.cursor()
    for row in c.execute('select * from personinfo where robot_id = ?;', [robot_id]):
        if -1 != row[0].find(robot_id):
            print "GetYear:%s"%row[2]
            return row[2]
def GetSex(robot_id):
    global db_conn
    c = db_conn.cursor()
    for row in c.execute('select * from personinfo where robot_id = ?;', [robot_id]):
        if -1 != row[0].find(robot_id):
            print "GetSex:%s"%row[3]
            return row[3]
def addToDB():
    global db_conn
    global PERSONINFO_DEFAULT
    db_conn.execute('insert into personinfo (robot_id, Name, Year, Sex, Parent, hometown, hobby) values(?, ?, ?, ?, ?, ?, ?);', PERSONINFO_DEFAULT)
    db_conn.commit()
def main():
    global client_speak
    global face_detected
    global lang
    global keywords_to_context
    global client_batteryquery
    global last_sentence
    #Init ROS
    reload(sys)
    sys.setdefaultencoding("utf-8")
    rospy.init_node('neo_questions')
    lang = rospy.get_param("/system_lang", "cn")
    last_sentence=""
    #Init variable to know if somebody is in front of qbo
    face_detected = False
    keywords_to_context={ 'smarthome':['关闭','打开','频道加','频道减','声音加','声音减'],
                               'motionctl':['前','后','左','右','停'],
                               'weather':['天气','热不热','温度', '几度', '多少度', '下雨', '有雨'],
                               'personinfo':['自我介绍','爸爸','妈妈','爱好','男','女','几岁','多大','家乡','美女','帅哥','特长'],
                               'education':['讲故事','背古诗','背唐诗','朗诵','背诵','阅读','朗读','静夜思','悯农'],
                               'media':['唱歌','播放','小老鼠上灯台','沙沙沙','小苹果'],
                               'batteryquery':['电量','多少电','电压够不够'],
                               'switch_voicetype':['四川话','普通话','陕西话','广东话','粤语','河南话'],
                               'jiujintai':['你好','名字','几岁','多大','项目介绍', '项目简介', '位置', '配套', '户型', '价格', '物业费', '公摊', '层高', '按揭', '供暖', '电梯费','天然气', '物业', '九锦一号', '交房',"智能公寓","面积","交房","多少钱","几梯几户","多少层","电梯费","水电费"],
                               'modeselect':['开启运动模式','关闭运动模式']}
    #Load plugins
    loadPlugins()
    read_smarthome_dic()
    read_weather_dic()
    set_language(lang)
    initDB("/home/runji/.ros/")
    if not IsinDB(ROBOT_ID):
        addToDB()
    print GetName(ROBOT_ID)
    print GetYear(ROBOT_ID)
    print GetSex(ROBOT_ID)
    print "Language loaded: "+lang
#    print "Dialog => %s"%dialogue
    for k in dialogue:
	print "%s:"%k,
        for element in dialogue[k]:
		print "%s"%element
        print ""
#    print "%s:%s"%(k,dialogue[k])
#    print "Dialog => "+str(dialogue)

    rospy.loginfo("Starting questions node")
 
# call "/say" service to speak selected words
    client_speak = rospy.ServiceProxy("/say", Text2Speach)
    client_batteryquery = rospy.ServiceProxy("query_battery", BatteryQuery)
    #Set Julius
    rospy.Subscriber("/system_lang", String, system_language)

    #For face view
    rospy.Subscriber("/qbo_face_tracking/face_pos_and_dist", FacePosAndDist, face_callback)

    rospy.spin()


if __name__ == '__main__':
    main()

