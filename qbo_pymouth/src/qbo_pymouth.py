#!/usr/bin/env python
import roslib; roslib.load_manifest('qbo_pymouth')
import rospy
import sys
import re
from qbo_arduqbo.msg import Mouth as Mouth_msg #Cambiar
#import MySQLdb
import sqlite3
import os
import types

def numberToMouthArray(shapeNumber):
    #create shape array from string number
    #shapeNumber = int(number)
    shapeBinString="{0:b}".format(shapeNumber)
    shape = [ 1 if n=='1' else 0 for n in shapeBinString ]
    while len(shape)<20:
        shape = [0] + shape
    shape.reverse()
    return shape

class Mouth:
    def __init__(self,idN,name,shape):
        if type(shape)==types.IntType:
            shape=numberToMouthArray(shape)
        self.idN=int(idN)
        self.name=str(name)
        self.shape=shape

class mouth:

    def __init__(self):
        self.conn = sqlite3.connect(os.environ["HOME"]+'/.mouthdb', check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.cursor=self.conn.cursor()
        self.vMouths=[]
        self.mouthValue=0
        self.mouth_pub=rospy.Publisher('/cmd_mouth', Mouth_msg)
        self.__chargeMouths()

    def __del__(self):
        print "Ending connection"
        self.kill()


    def kill(self):
        print "Killing connection"
        try:
            self.conn.close()
        except sqlite3.OperationalError:
            print sqlite3.OperationalError
            print "Couldn't close connection. Probably it have been closed previously"
	
    def sendMouthPr1(self,mo):
        boca=Mouth_msg()
        boca.mouthImage=mo.shape
        #print mo.shape
        self.mouth_pub.publish(boca)

    def changeMouth(self,value):
        if int(value) > len(self.vMouths):
            return "KO"
        for mo in self.vMouths:
            if mo.idN == int(value):
                self.sendMouthPr1(mo)
                self.value=int(value)
                return "OK"
        return "KO"

    def changeMouth2(self,shape):
        mo=Mouth(-1,"none",shape)
        self.sendMouthPr1(mo)
        return "OK"

    def getMouths(self):
        result = ""
        for mouth in self.vMouths:
            result += str(mouth.idN) + ","
            for i in range(20):
                result += str(mouth.shape[i]) + ","
            result += mouth.name + "|"
        result = result.strip('|')
        print "getMouths(): " + result
        return result
        
    def __createMouthsSQL(self):
        #comprobar cursor
        self.cursor.execute("drop table if exists pr1_mouths");
        self.cursor.execute("create table pr1_mouths (id int primary key, name varchar(255), shape int)");
        self.cursor.execute("delete from pr1_mouths");
        self.cursor.execute("insert into pr1_mouths (id,name,shape) values (0,'Happy',476160)");
        self.cursor.execute("insert into pr1_mouths (id,name,shape) values (1,'Sad',571392)");
        self.cursor.execute("insert into pr1_mouths (id,name,shape) values (2,'Ooh',476718)");
        self.cursor.execute("insert into pr1_mouths (id,name,shape) values (3,'Pucker the mouth to the right',17376)");
        self.cursor.execute("insert into pr1_mouths (id,name,shape) values (4,'Pucker the mouth to the left',2016)");
        self.cursor.execute("insert into pr1_mouths (id,name,shape) values (5,'Straight face',31744)");
        self.cursor.execute("insert into pr1_mouths (id,name,shape) values (6,'Small mouth',141636)");
        self.cursor.execute("insert into pr1_mouths (id,name,shape) values (7,'Speak 1',31)");
        self.cursor.execute("insert into pr1_mouths (id,name,shape) values (8,'Speak 2',479)");
        self.cursor.execute("insert into pr1_mouths (id,name,shape) values (9,'Speak 3',14911)");
        self.cursor.execute("insert into pr1_mouths (id,name,shape) values (10,'Speak 4',15359)");
        self.cursor.execute("insert into pr1_mouths (id,name,shape) values (11,'Speak 5',476735)");
        self.cursor.execute("insert into pr1_mouths (id,name,shape) values (12,'Speak 6',491519)");
        self.cursor.execute("insert into pr1_mouths (id,name,shape) values (13,'None',0)");
        self.cursor.execute("insert into pr1_mouths (id,name,shape) values (14,'surprise',476718)");
        self.cursor.execute("insert into pr1_mouths (id,name,shape) values (15,'regular',69904)");
        self.cursor.execute("insert into pr1_mouths (id,name,shape) values (16,'tongue',283616)");
        self.conn.commit()



    def __resetMouths(self):
        print 'no mouths. reseting them'
        self.vMouths=[]

        self.vMouths.append(Mouth(0,"Happy",476160,));
        self.vMouths.append(Mouth(1,"Sad",571392));
        self.vMouths.append(Mouth(2,"Ooh",476718));
        self.vMouths.append(Mouth(3,"Pucker the mouth to the right",17376));
        self.vMouths.append(Mouth(4,"Pucker the mouth to the left",2016));
        self.vMouths.append(Mouth(5,"Straight face",31744));
        self.vMouths.append(Mouth(6,"Small mouth",141636));
        self.vMouths.append(Mouth(7,"Speak 1",31));
        self.vMouths.append(Mouth(8,"Speak 2",479));
        self.vMouths.append(Mouth(9,"Speak 3",14911));
        self.vMouths.append(Mouth(10,"Speak 4",15359));
        self.vMouths.append(Mouth(11,"Speak 5",476735));
        self.vMouths.append(Mouth(12,"Speak 6",491519));
        self.vMouths.append(Mouth(13,"None",0));

        self.vMouths.append(Mouth(14,"surprise",476718));
        self.vMouths.append(Mouth(15,"regular",69904));
        self.vMouths.append(Mouth(16,"tongue",283616));

        self.__createMouthsSQL()

    def __chargeMouths(self):
        #comprobamos conexion
        self.vMouths=[]
        sql="select id,name,shape from pr1_mouths order by id"
        try:
            self.cursor.execute(sql)
            resultado=self.cursor.fetchall()
            for registro in resultado:
                #create shape array from string number
                shape = numberToMouthArray(int(registro[2]))
                self.vMouths.append(Mouth(int(registro[0]),registro[1],shape))
            if len(self.vMouths)<16:
                self.__resetMouths()
        except Exception, e:
            print e
            self.__resetMouths()

    def addMouth(self, name, iShape):
        if not name == None and len(name)>0 and int(iShape) >= 0 and int(iShape) <= 1048576:
            name=name.strip()
            for mouth in self.vMouths:
                if name == mouth.name:
                    return
            self.cursor.execute("select max(id) from pr1_mouths")
            resultado=self.cursor.fetchone()
            iId=resultado[0]+1
            if(iId>16):
                orden="insert into pr1_mouths (id,name,shape) values (" + str(iId) + ",'" + str(name) + "'," + iShape + ")"
                print orden
                self.cursor.execute(orden)
                self.conn.commit()
                shape = numberToMouthArray(int(iShape))
                self.vMouths.append(Mouth(iId,name,shape))
                self.changeMouth(iId)
        return ""

    def mdfMouth(self, iId, name, iShape):
        if int(iId) > 16 and name != None and len(name)>0 and int(iShape) >= 0 and int(iShape) <= 1048576:
            name=name.strip()
            selectedMouth = []
            for mouth in self.vMouths:
                if mouth.idN != int(iId) and name == mouth.name:
                    return
                elif mouth.idN == int(iId):
                    mouth.name = name
                    #create shape array from string number
                    shape = numberToMouthArray(int(iShape))
                    mouth.shape = shape
            self.cursor.execute("update pr1_mouths set name = '" + name + "', shape = " + iShape +
                                        " where id = " + iId)
            self.conn.commit()
            self.changeMouth(iId)
        return ""

    def delMouth(self, iId):
        if int(iId) > 16:
            pos=-1
            for mouth in self.vMouths:
                if mouth.idN == int(iId):
                    pos = self.vMouths.index(mouth)
                    self.cursor.execute("delete from pr1_mouths where id = " + iId)
            if pos != -1:
                self.vMouths.pop(pos)
        self.conn.commit()
        return ""

'''
import time
import roslib
roslib.load_manifest('qbo_pymouth')

rospy.init_node('qbo_pymouth')

m = mouth()
for i in range(16):
    print m.changeMouth(i)
    time.sleep(1)
'''
