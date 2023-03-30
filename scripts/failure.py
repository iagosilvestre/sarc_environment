#!/usr/bin/python3

import rospy
import rospkg
from gazebo_msgs.srv import GetModelState
from gazebo_msgs.msg import ModelState
from gazebo_msgs.srv import SetModelState
import rosnode
import math

from mrs_msgs.msg import UavManagerDiagnostics as UavManagerDiagnostics
from mavros_msgs.srv import CommandBool as CommandBool
from std_srvs.srv import Trigger as Trigger
from gazebo_msgs.srv import DeleteModel, DeleteModelRequest, ApplyBodyWrench
from geometry_msgs.msg import Point, Wrench, Vector3

from nav_msgs.msg import Odometry
from std_msgs.msg import Header, Float64
from gazebo_msgs.srv import GetLinkState, GetLinkStateRequest

global uav_name
uav_name = "uav1"
class Landing:
    def callback(self, data):
        x_pub=rospy.Publisher ('/failure_uav1', Int8)
        y_pub=rospy.Publisher ('/agent_detected_failure_uav1', Int8)
        xfail = Int8()
        xfail = 1

        r = rospy.Rate(2)


        while not rospy.is_shutdown():

            #print(xland)
            #print(yland)
            x_pub.publish (xfail)
            r.sleep()
            rospy.signal_shutdown("yes")

    def __init__(self):

        rospy.init_node('failure', anonymous=True) 
        self.subscriber = rospy.Subscriber('/' + uav_name + '/uav_manager/diagnostics', UavManagerDiagnostics, self.callback)
        self.motor1 = rospy.ServiceProxy('/uav1/control_manager/motors', CommandBool)
        rospy.loginfo('initialized')
        rospy.spin()

if __name__ == '__main__':
    try:
        node_crash_checker = Landing()
    except rospy.ROSInterruptException:
        pass
