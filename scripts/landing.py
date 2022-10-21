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
        x_pub=rospy.Publisher ('/landing_x', Float64)
        y_pub=rospy.Publisher ('/landing_y', Float64)

        rospy.wait_for_service ('/gazebo/get_link_state')
        get_link_srv = rospy.ServiceProxy('/gazebo/get_link_state', GetLinkState)

        xland = Float64()
        yland = Float64()

        link = GetLinkStateRequest()
        link.link_name='SARclandArea::link'
        r = rospy.Rate(2)


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
        self.subscriber = rospy.Subscriber('/' + uav_name + '/uav_manager/diagnostics', UavManagerDiagnostics, self.callback)
        rospy.loginfo('initialized')
        rospy.spin()

if __name__ == '__main__':
    try:
        node_crash_checker = Landing()
    except rospy.ROSInterruptException:
        pass
