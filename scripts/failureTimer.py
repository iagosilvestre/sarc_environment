#!/usr/bin/python3

import rospy
import rospkg
import rosnode
import math
import time

from mrs_msgs.msg import UavManagerDiagnostics as UavManagerDiagnostics
from mrs_msgs.srv import String as mrsString
from mavros_msgs.srv import CommandBool as CommandBool
from std_srvs.srv import Trigger as Trigger
from std_srvs.srv import SetBool as SetBool
from gazebo_msgs.srv import DeleteModel, DeleteModelRequest, ApplyBodyWrench
from geometry_msgs.msg import Point, Wrench, Vector3

from nav_msgs.msg import Odometry
from std_msgs.msg import Header, Float64, Int8,String,Bool
from gazebo_msgs.srv import GetLinkState, GetLinkStateRequest



class FailureTimer:
    def __init__(self):
        # Create a ROS publisher
        self.percept_pub=rospy.Publisher ('/failure_uav1', Int8, queue_size=1)
        self.motor1 = rospy.ServiceProxy('/uav1/control_manager/motors', SetBool)
        self.tracker = rospy.ServiceProxy('/uav1/control_manager/switch_tracker', mrsString)
        # Initialize temperature data
        self.temperature = 0
    def perception(self, event=None):
        msg = Int8()
        msg.data = 1
        self.percept_pub.publish(msg)
        self.motor1(0) 
        time.sleep(1)
        msg.data = 0
        self.percept_pub.publish(msg)
    def reaction(self, data):
        self.motor1(1)
        self.tracker('LandoffTracker')
        
        
        
        
if __name__ == '__main__':
    rospy.init_node("failureTimer")
    # Create an instance of Temperature sensor
    ft = FailureTimer()
    rospy.Subscriber('/agent_detected_failure_uav1', String, ft.reaction)
    # Create another ROS Timer for publishing data
    rospy.Timer(rospy.Duration(10.0/1.0), ft.perception)
    # Don't forget this or else the program will exit
    rospy.spin()
