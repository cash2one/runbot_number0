#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Authors: Miguel Angel Julian <miguel.a.j@openqbo.com>
#
# modifié par Vincent FOUCAULT <elpimous12@orange.fr>
#
# - programme de déplacement aléatoire pour QBO, avec
# prise en compte du vide, de la chute arrière, du blocage.
#
# - mise en oeuvre des capteurs à ultrason SRF10,
# - mise en oeuvre du capteur à IR GP2Y0A21YK
# - mise en oeuvre de l'imu QBOARD 4
# - utilisation de l'odométrie
#
###################################################

import roslib; roslib.load_manifest('neo_deplacement_aleatoire')
import os
import rospy
import threading
from sensor_msgs.msg import PointCloud # les srf10
from sensor_msgs.msg import Imu # Je sais pas ! Peut-être l' imu !
from nav_msgs.msg import Odometry # infos des moteurs de roues
from lib_qbo_pyarduqbo import qbo_control_client
from time import sleep # sert a creer soit des pauses, soit des temps d'éxécution de commandes
from random import choice, uniform
from math import atan, atan2 # sert a la prise d'angle

from neo_talk.srv import Text2Speach # read service content (words we want to be spoken)

angular_speed=0.10
lineal_speed=0.10
obstacles=False
l_imu=""
floor=""

def speak_this(text):
   global client_speak
   client_speak(str(text))

class neo_deplacement_aleatoire():
    global client_speak
    def __init__(self):
        self.qbo_controller=qbo_control_client()
        self.obstacles=False
        self.solMax=35
        self.solMin=10
        self.angle=-1.9 # angle maxi avant gestion de chute arrière, Ligne 71
        self.no_floor=True
        self.floorObstacle=True
        self.too_imu_angle=True
        self.blocked=True
        self.sensors_distance=0.215 #distance entre capteurs, sert a calculer l'angle, Ligne 129
        self.lineal_speed=0.0
        self.angular_speed=0.0
        self.turn_time=0.1
        self.wall_distance_limit=0.4
        self.last_turn_direction=False # signifie tourne a droite
        self.uniform_lineal_speed_change=0.06 # permet un peu de variation de vitesse en ligne droite
        self.sentences=['mais ya des murs partout? dans cette piaice','','mince','sait la galère avec ces murs','','','','y aurai pas un mur? la?','','','bon, encore un mur','','','j en ai marre de ces murs','','bon? vincent? il est pourri ton programme']

        self.sentences_chute=['Attention, je vais tomber','jai le vertige','rattrappe-moi','il faut que je recule', 'je vais tomber','vite','attention']

        rospy.Subscriber('/distance_sensors_state/floor_sensor', PointCloud, self.capt_sol, queue_size=1)
        rospy.Subscriber('/imu_state/data',Imu,self.ImuCallback, queue_size=1)
	rospy.Subscriber('/odom', Odometry, self.odometry, queue_size=1)

    def capt_sol(self,data): # floor_sensor
        if (data.points[0].x >= self.solMax):
            self.no_floor=True
            speak_this(choice(self.sentences_chute))
            print " *** ATTENTION, CHUTE IMMINENTE !!! ***"
        else:
            self.no_floor=False 
            print "                           sol ok"

        if (data.points[0].x <= self.solMin):
            self.floorObstacle=True
        else:
            self.floorObstacle=False 
   

    def ImuCallback(self,data): # imu (x)
        if data.linear_acceleration.x < self.angle:
            self.too_imu_angle=True
        else:
            self.too_imu_angle=False        


    def odometry(self,data): # condition d'immobilisation / blocking condition
        #print "j'avance à ",data.twist.twist.linear.x
        if data.twist.twist.linear.x == 0.0:
            sleep(1)
            if data.twist.twist.linear.x == 0.0:
                self.blocked=True
        else:
            self.blocked=False


    def spin(self):
        global obstacles
        global l_imu
        global floor
        global client_speak

        # call "/say" service to speak selected words
        client_speak = rospy.ServiceProxy("/say", Text2Speach)

        while(not rospy.is_shutdown()):
           while self.too_imu_angle==False or self.no_floor==False: # tant qu'il a absence de vide ou d'inclinaison arrière..
              frontal_distances=self.qbo_controller.getFrontalDistances()
              now=rospy.Time.now()
              warning_left_flag=False
              warning_right_flag=False
              if frontal_distances[0][1] and (now-frontal_distances[0][1])<rospy.Duration(0.5):
                  warning_left_flag=True
              if frontal_distances[1][1] and (now-frontal_distances[1][1])<rospy.Duration(0.5):
                  warning_right_flag=True

              left_distance=999.9
              right_distance=999.9

              if warning_left_flag:
                 left_distance=frontal_distances[0][0]
              if warning_right_flag:
                 right_distance=frontal_distances[1][0]
              if not warning_left_flag or not warning_right_flag:

                 if left_distance<right_distance: # si QBO voit un obstacle de loin, il commence à tourner.
                    if self.lineal_speed != 0:
                       self.last_turn_direction=False
                       self.lineal_speed=0.20+uniform(-self.uniform_lineal_speed_change,self.uniform_lineal_speed_change)
                       self.angular_speed=-angular_speed+uniform(-self.uniform_lineal_speed_change,self.uniform_lineal_speed_change)
                       self.last_turn_direction=False

                 elif left_distance>right_distance:
                    if self.lineal_speed != 0:
                       self.last_turn_direction=True
                       self.lineal_speed=0.20+uniform(-self.uniform_lineal_speed_change,self.uniform_lineal_speed_change)
                       self.angular_speed=angular_speed+uniform(-self.uniform_lineal_speed_change,self.uniform_lineal_speed_change)
                       self.last_turn_direction=True

                 else: # pas d'obstacles
                    self.lineal_speed=0.30+uniform(-self.uniform_lineal_speed_change,self.uniform_lineal_speed_change)
                    self.angular_speed=0.0+uniform(-self.uniform_lineal_speed_change,self.uniform_lineal_speed_change)
                    obstacles=False

              else: # calcul de prise d'angle
                 angle=atan2((left_distance-right_distance),self.sensors_distance)
                 self.lineal_speed=lineal_speed+uniform(-self.uniform_lineal_speed_change,self.uniform_lineal_speed_change)
                 min_distance=min(left_distance,right_distance)
                 time_limit=min_distance/self.lineal_speed
                 if min_distance<=0 or time_limit==0:
                    self.qbo_controller.setLinearAngular((self.lineal_speed+uniform(-0.03,0.03)),self.angular_speed+uniform(-0.1,0.1))
                 else:
                    self.angular_speed=angle/time_limit

              if (left_distance<self.wall_distance_limit) and (right_distance<self.wall_distance_limit) or self.floorObstacle==True:
                 speak_this(choice(self.sentences))
                 print " obstacle de proximité "
                 if not obstacles:
                    obstacles=True
                 break

              else:
                 obstacles=False
                 self.turn_time=0.15
              self.qbo_controller.setLinearAngular(self.lineal_speed,self.angular_speed)
              sleep(self.turn_time)

           # ...sinon je recule sur 3 secondes, tourne sur 3 secondes dans le bon sens, puis reprends mon chemin.
           for f in range(2):
              print " arrière"
              self.qbo_controller.setLinearAngular((-0.20+uniform(-0.03,0.03)),0.0)
              sleep(1)

           if self.last_turn_direction:
              for d in range(2):
                 print " arrière gauche"
                 self.qbo_controller.setLinearAngular(0.0,(0.3+uniform(-0.2,0.2)))
                 sleep(1)
           else:
              for g in range(2):
                 print " arrière droite"
                 self.qbo_controller.setLinearAngular(0.0,(-0.3+uniform(-0.2,0.2)))
                 sleep(1)
                  
           self.qbo_controller.setLinearAngular(self.lineal_speed,self.angular_speed)
           sleep(0.15)


if __name__ == "__main__":
    #try:
        rospy.init_node('neo_deplacement_aleatoire')
        random_controller=neo_deplacement_aleatoire()
        random_controller.spin()





