#!/usr/bin/env python
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

class motorFailure:
    def __init__(self):
        # Initialize node
        rospy.init_node('motor_failure')

        #critical things
        self.reaction_times = []
        self.perception_times = []

        # Create publisher
        self.percept_pub=rospy.Publisher ('/failure_uav1', Int8, queue_size=1)
        self.motor1 = rospy.ServiceProxy('/uav1/control_manager/motors', SetBool)
        self.tracker = rospy.ServiceProxy('/uav1/control_manager/switch_tracker', mrsString)
        self.ctd = 0
        self.isFinished = False
        self.file = open("ariacReactionTimes.log", "w")
        self.startTime = time.time()

        # Create subscriber
        rospy.Subscriber('/agent_detected_failure_uav1', String, self.reaction)
        rospy.Subscriber('finish', Bool, self.callback2)

    def run(self):
        rate = rospy.Rate(0.1) # 0.1 Hz
        msg = Int8()
        while not (rospy.is_shutdown() or self.isFinished):
            # Publish message
            msg.data = 1
            self.percept_pub.publish(msg)
            self.motor1(0) 
            self.perception_times.append(time.perf_counter())
            time.sleep(1)
            msg.data = 0
            self.percept_pub.publish(msg)
            rate.sleep()
        self.recordTimes()
        rospy.signal_shutdown('Node is shutting down.')

    def recordTimes(self):
        if len(self.perception_times) == len(self.reaction_times):
            for pTime, rTime in zip(self.perception_times, self.reaction_times):
                elapsed_time = (rTime - pTime) * 1000 
                self.file.write(f"{pTime}\t{rTime}\t{elapsed_time}\n")
        else:
            pIter = iter(self.perception_times)
            next(pIter)
            for rTime in self.reaction_times:
                pTime = next(pIter)
                elapsed_time = (rTime - pTime) * 1000 
                self.file.write(f"{pTime}, {rTime}, {elapsed_time}\n")
        total_time = time.time()-self.startTime        
        if not self.file.closed:
            self.file.write(f"Sent msgs: {len(self.perception_times)}\n")
            self.file.write(f"Received msgs: {len(self.reaction_times)}\n")
            self.file.write(f"Elapsed_time(s): {total_time}\n")
            self.file.close()


    def reaction(self, message):
        # Print received message
        self.reaction_times.append(time.perf_counter())
        self.motor1(1)
        self.tracker('MpcTracker')
        rospy.loginfo("Received msg: %s", message.data)
        

    def callback2(self, message):
        # Print received message
        self.isFinished = True
        rospy.loginfo("FINISHED")

if __name__ == '__main__':
    node = motorFailure()
    time.sleep(1)
    node.run()
