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
        
        x_pub=rospy.Publisher ('/landing_x', Float64,queue_size=10)
        y_pub=rospy.Publisher ('/landing_y', Float64,queue_size=10)

        rospy.wait_for_service ('/gazebo/get_link_state')
        get_link_srv = rospy.ServiceProxy('/gazebo/get_link_state', GetLinkState)

        xland = Float64()
        yland = Float64()

        link = GetLinkStateRequest()
        link.link_name='SARclandArea::link'
        r = rospy.Rate(1)


        while not rospy.is_shutdown():
            result = get_link_srv(link)

            xland.data = result.link_state.pose.position.x
            yland.data = result.link_state.pose.position.y

            #print(xland)
            #print(yland)
            x_pub.publish (xland)
            y_pub.publish (yland)
            r.sleep()
            #rospy.signal_shutdown("yes")

    def __init__(self):

        rospy.init_node('landing', anonymous=True) 

        self.delete = rospy.ServiceProxy('/gazebo/delete_model', DeleteModel)    
        self.subscriber = rospy.Subscriber('/' + uav_name + '/uav_manager/diagnostics', UavManagerDiagnostics, self.callback)
        self.arm1 = rospy.ServiceProxy('/' + uav_name + '/mavros/cmd/arming', CommandBool)
        self.arm2 = rospy.ServiceProxy('/uav2/mavros/cmd/arming', CommandBool)
        self.arm3 = rospy.ServiceProxy('/uav3/mavros/cmd/arming', CommandBool)
        self.arm4 = rospy.ServiceProxy('/uav4/mavros/cmd/arming', CommandBool)
        self.arm5 = rospy.ServiceProxy('/uav5/mavros/cmd/arming', CommandBool)
        self.arm6 = rospy.ServiceProxy('/uav6/mavros/cmd/arming', CommandBool)
        self.activate1 = rospy.ServiceProxy('/' + uav_name + '/uav_manager/midair_activation', Trigger)
        self.activate2 = rospy.ServiceProxy('/uav2/uav_manager/midair_activation', Trigger)
        self.activate3 = rospy.ServiceProxy('/uav3/uav_manager/midair_activation', Trigger)
        self.activate4 = rospy.ServiceProxy('/uav4/uav_manager/midair_activation', Trigger)
        self.activate5 = rospy.ServiceProxy('/uav5/uav_manager/midair_activation', Trigger)
        self.activate6 = rospy.ServiceProxy('/uav6/uav_manager/midair_activation', Trigger)
        self.apply_wrench = rospy.ServiceProxy('/gazebo/apply_body_wrench', ApplyBodyWrench)
        
        rospy.loginfo('initialized')
        rospy.spin()

if __name__ == '__main__':
    try:
        node_crash_checker = Landing()
    except rospy.ROSInterruptException:
        pass
