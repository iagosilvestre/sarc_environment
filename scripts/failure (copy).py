#!/usr/bin/python3

import rospy
import rospkg
from gazebo_msgs.srv import GetModelState
from gazebo_msgs.msg import ModelState
from gazebo_msgs.srv import SetModelState
import rosnode
import math

from mrs_msgs.msg import UavManagerDiagnostics as UavManagerDiagnostics
from mrs_msgs.srv import String as mrsString
from mavros_msgs.srv import CommandBool as CommandBool
from std_srvs.srv import Trigger as Trigger
from std_srvs.srv import SetBool as SetBool
from gazebo_msgs.srv import DeleteModel, DeleteModelRequest, ApplyBodyWrench
from geometry_msgs.msg import Point, Wrench, Vector3

from nav_msgs.msg import Odometry
from std_msgs.msg import Header, Float64, Int8,String
from gazebo_msgs.srv import GetLinkState, GetLinkStateRequest
myvar = None
global uav_name
uav_name = "uav1"


class Failure:
    def some_callback(self,data):
        global myvar
        myvar = data
        rospy.loginfo('Agent detected failure in motors: ' + str(data))
        rospy.loginfo('Turning motors back on')
        self.motor1(1) 
        #rospy.loginfo('Swapping to landoff Tracker')
        #self.tracker('LandoffTracker')
        rospy.loginfo('Initializing landing')
        self.land()
        

    def callback(self, data):
        x_pub=rospy.Publisher ('/failure_uav1', Int8, queue_size=1)
        count=1
        rospy.Subscriber('/agent_detected_failure_uav1', String, self.some_callback)

        r = rospy.Rate(2)
        
        while not rospy.is_shutdown():
            if (count == 1):
                rospy.loginfo('Turning off motors')
                self.motor1(0) 
            x_pub.publish(1)
            r.sleep()
            count+=1
            #rospy.signal_shutdown("yes")

    def __init__(self):

        rospy.init_node('failure', anonymous=True) 
        self.subscriber = rospy.Subscriber('/' + uav_name + '/uav_manager/diagnostics', UavManagerDiagnostics, self.callback)
        self.motor1 = rospy.ServiceProxy('/uav1/control_manager/motors', SetBool)
        self.tracker = rospy.ServiceProxy('/uav1/control_manager/switch_tracker', mrsString)
        self.land = rospy.ServiceProxy('/uav1/uav_manager/land', Trigger)
        rospy.loginfo('initialized')
        rospy.spin()

if __name__ == '__main__':
    try:
        node_crash_checker = Failure()
    except rospy.ROSInterruptException:
        pass
