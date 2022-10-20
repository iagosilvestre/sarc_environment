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

class Activator:
    def callback(self, data):
        body_name = uav_name + '::base_link'
        body_name2 = 'uav2::base_link'
        body_name3 = 'uav3::base_link'
        body_name4 = 'uav4::base_link'
        body_name5 = 'uav5::base_link'
        body_name6 = 'uav6::base_link'
        wrench = Wrench()
        force = [3, 3, 3]
        wrench.force = Vector3(*force)
        duration = rospy.Duration(15)
        rospy.sleep(15)

        self.arm1(1)
        self.arm2(1)
        self.arm3(1)
        self.arm4(1)
        self.arm5(1)
        self.arm6(1)
        #armAll(1)

        dele = DeleteModelRequest()
        dele.model_name = "SARckc_floor"
        self.delete(dele)
        rospy.sleep(0.2)

        self.activate1()
        self.activate2()
        self.activate3()
        self.activate4()
        self.activate5()
        self.activate6()
        #activateAll()
        rospy.sleep(1)
        rospy.loginfo('applying')
        self.apply_wrench(body_name, 'world', Point(0, 0, 0), wrench, rospy.Time().now(), duration)
        self.apply_wrench(body_name2, 'world', Point(0, 0, 0), wrench, rospy.Time().now(), duration)
        self.apply_wrench(body_name3, 'world', Point(0, 0, 0), wrench, rospy.Time().now(), duration)
        self.apply_wrench(body_name4, 'world', Point(0, 0, 0), wrench, rospy.Time().now(), duration)
        self.apply_wrench(body_name5, 'world', Point(0, 0, 0), wrench, rospy.Time().now(), duration)
        self.apply_wrench(body_name6, 'world', Point(0, 0, 0), wrench, rospy.Time().now(), duration)
        #rospy.signal_shutdown("yes")

        x_pub=rospy.Publisher ('/landing_x', Float64,queue_size=10)
        y_pub=rospy.Publisher ('/landing_y', Float64,queue_size=10)

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

        rospy.init_node('activator', anonymous=True) 

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
        node_crash_checker = Activator()
    except rospy.ROSInterruptException:
        pass
