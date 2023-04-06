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
from std_msgs.msg import Header, Float64, Int8,String,Bool
from gazebo_msgs.srv import GetLinkState, GetLinkStateRequest

from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener
from tf2_ros import TransformException

class Failure:
    def __init__(self):
        rospy.init_node('failure', anonymous=True)
        rospy.loginfo('initialized')
        #critical things
        self.reaction_times = []
        self.perception_times = []
        
    
        # Subscribers
        self.go_home_sub = rospy.Subscriber(Bool, '/ariac_human/go_home', self.go_home, 10) #
        self.go_home_agv_sub = self.create_subscription(Bool, '/ariac_human/go_home_agv', self.go_home_agv, 10)
        self.send_to_goal_sub = self.create_subscription(Point, '/ariac_human/goal_position', self.send_to_goal, 10)
        self.critical_reaction_sub = self.create_subscription(String, '/agent_detected_failure_uav1', self.critical_reaction, 10)
        self.start_sub = self.create_subscription(Bool, '/ariac/start_human', self.start_human, 10)

        # Timer
        self.first_pub = True
        self.timer_rate = 0.1
        self.update_timer = self.create_timer(self.timer_rate, self.on_update)

        # Publisher: CRITICAL PERCEPTION
        self.critical_perception_pub = self.create_publisher(topic='/failure_uav1', 
                                                         msg_type=Int8, qos_profile = 10)

        #
        self.has_started = False
        self.count = 0
        self.file = open("ariacReactionTimes.log", "w")
        self.startTime = time.time()
        
    def stop_human(self, msg: Bool):
        if msg.data:
            self.navigator.cancelTask()
            self.has_active_goal = False

    def go_home(self, msg: Bool):
        #Save the log file for critical things (time in millisenconds: *1000)
        if len(self.perception_times) == len(self.reaction_times):
            for pTime, rTime in zip(self.perception_times, self.reaction_times):
                elapsed_time = (rTime - pTime) * 1000 
                self.file.write(f"{pTime}\t{rTime}\t{elapsed_time}\n")
        else:
            pIter = iter(self.perception_times)
            for rTime in self.reaction_times:
                pTime = next(pIter)
                elapsed_time = (rTime - pTime) * 1000 
                # if elapsed_time > 2500:
                #     self.file.write("11111.11111\n")
                #     try:
                #          pTime = next(pIter)
                #     except StopIteration:
                #         print("Vector perception_times is exhausted")
                #         break
                #     elapsed_time = (rTime - pTime) * 1000

                # if elapsed_time > 2500:
                #     self.file.write("11111.11111\n")
                #     try:
                #          pTime = next(pIter)
                #     except StopIteration:
                #         print("Vector perception_times is exhausted")
                #         break
                #     elapsed_time = (rTime - pTime) * 1000

                # if elapsed_time > 2500:
                #     self.file.write("11111.11111\n")
                #     try:
                #          pTime = next(pIter)
                #     except StopIteration:
                #         print("Vector perception_times is exhausted")
                #         break
                #     elapsed_time = (rTime - pTime) * 1000
                # self.file.write(f"{elapsed_time}\n")
                self.file.write(f"{pTime}, {rTime}, {elapsed_time}\n")
        total_time = time.time()-self.startTime        
        if not self.file.closed:
            self.file.write(f"Sent msgs: {len(self.perception_times)}\n")
            self.file.write(f"Received msgs: {len(self.reaction_times)}\n")
            self.file.write(f"Elapsed_time(s): {total_time}\n")
            self.file.close()
        rospy.signal_shutdown("yes")

        if msg.data:
            self.navigator.cancelTask()
            self.navigator.setInitialPose(self.initial_pose)

            self.has_active_goal = False
            self.teleport_human_client.call_async(self.teleport_request)
            self.s_zone_penalty_client.call_async(self.safe_zone_penalty_request)

    def go_home_agv(self, msg: Bool):
        if msg.data:
            self.navigator.cancelTask()
            self.navigator.setInitialPose(self.initial_pose)

    def send_to_goal(self, msg: Point):
        self.has_active_goal = True

        self.goal_pose.pose.position.x = msg.x
        self.goal_pose.pose.position.y = msg.y
        self.goal_pose.pose.position.z = msg.z
        
        self.navigator.goToPose(self.goal_pose)

    # Added to test Critical Things 
    def critical_reaction(self, msg: String):
        # Add the current time to the message_times list
        rospy.ServiceProxy('/uav1/control_manager/motors', 1)
        self.reaction_times.append(time.perf_counter())

    # Support 4 Critical Things: start critical perceptions
    def start_human(self, msg: Bool):
        self.has_started = True
        self.count = 0


        # Extra call to test Critical Things: 
        # Param 0.0 means fixed-periodic, otherwise a probability up to 1.0
        self.count = self.count + 1
        self.generate_criticalPercept(0.0)

    # ZERO probability means sending messages at every 3s (30 steps), should be 25 in total
    def generate_criticalPercept(self, probability: float):
        step = 10
        if probability > 0.0:
            if (random.random() <= probability) and self.has_started:
                msg = Bool()
                msg.data = True
                self.critical_perception_pub.publish(msg)
                self.perception_times.append(time.perf_counter())
        elif self.count < (step*40)+5:
            if (self.count % step)==0 and self.has_started:
                msg = Int8()
                msg.data = 1
                self.critical_perception_pub.publish(msg)
                rospy.ServiceProxy('/uav1/control_manager/motors', 0)
                self.perception_times.append(time.perf_counter())
if __name__ == '__main__':
    try:
        node_crash_checker = Failure()
    except rospy.ROSInterruptException:
        pass
