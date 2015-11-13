#!/usr/bin/env python
#-*- coding:utf-8 -*-
import roslib;roslib.load_manifest('qbo_wander')
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import PointCloud
class wander:
    
    def __init__(self):
        self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist)
        rospy.init_node('qbo_wander')
        self.speed = rospy.get_param("~start_speed", 0.2)
        self.angular_speed = rospy.get_param("~start_angular_speed", 0.5)	
        print "wander speed:%s agular_speed:%s"%(self.speed,self.angular_speed)
        self.cmd_vel = Twist()
        self.safety_limit = 50
        self.front_left = 65535
        self.front_right = 65535
        self.back_left = 65535
        self.back_right = 65535
        self.cmd_vel.linear.x = 0
        self.cmd_vel.angular.z = 0
        self.last_state_running = 0
        
        self.sub_back_left   = rospy.Subscriber('/distance_sensors_state/back_left_srf10', PointCloud, self.scan_back_left_callback)
        self.sub_back_right  = rospy.Subscriber('/distance_sensors_state/back_right_srf10', PointCloud, self.scan_back_right_callback)
        self.sub_front_left  = rospy.Subscriber('/distance_sensors_state/front_left_srf10', PointCloud, self.scan_front_left_callback)
        self.sub_front_right = rospy.Subscriber('/distance_sensors_state/front_right_srf10', PointCloud, self.scan_front_right_callback)
    def scan_front_left_callback(self, scan):
        self.front_left= scan.points[0].x
        print "front_left:%s"%scan.points[0].x
    def scan_front_right_callback(self, scan):
        self.front_right= scan.points[0].x
        print "front_right:%s"%scan.points[0].x
    def scan_back_left_callback(self, scan):
        self.back_left = scan.points[0].x
        print "back_left:%s"%scan.points[0].x
    def scan_back_right_callback(self, scan):
        self.back_right = scan.points[0].x
        print "back_right:%s"%scan.points[0].x
    def run(self):
        # We have to keep publishing the cmd_vel message if we want the robot to keep moving.
        while not rospy.is_shutdown():
            if self.front_left < self.safety_limit and self.front_right < self.safety_limit:
               self.cmd_vel.linear.x = -self.speed
               self.cmd_vel.angular.z = 0
            elif self.front_left < self.safety_limit:
               self.cmd_vel.linear.x = 0
               self.cmd_vel.angular.z = -self.angular_speed
            elif self.front_right < self.safety_limit:
               self.cmd_vel.linear.x = 0
               self.cmd_vel.angular.z = self.angular_speed
	    elif self.back_left < self.safety_limit and self.back_right < self.safety_limit:
               self.cmd_vel.linear.x = self.speed
               self.cmd_vel.angular.z = 0
            elif self.back_left < self.safety_limit:
               self.cmd_vel.linear.x = 0
               self.cmd_vel.angular.z = -self.angular_speed
            elif self.back_right < self.safety_limit:
               self.cmd_vel.linear.x = 0
               self.cmd_vel.angular.z = self.angular_speed
            else:
               self.cmd_vel.linear.x = 0
               self.cmd_vel.angular.z = 0
               if self.last_state_running == 1:
                   self.cmd_vel_pub.publish(self.cmd_vel)
                   self.last_state_running = 0
                   print "wander stop............"
            if(self.cmd_vel.linear.x !=0 or self.cmd_vel.angular.z !=0):
               self.last_state_running = 1
               self.cmd_vel_pub.publish(self.cmd_vel)
               print "wander speed:%s ang_speed:%s....."%(self.cmd_vel.linear.x, self.cmd_vel.angular.z)
               self.front_left = 65535
               self.front_right = 65535
               self.back_left = 65535
               self.back_right = 65535
            rospy.sleep(1)   
if __name__ == '__main__':
   controller = wander()
   try:
       controller.run()
   except rospy.ROSInterruptException:
#ROSInterruptException:
       pass
