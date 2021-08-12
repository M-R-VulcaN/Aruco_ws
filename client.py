#!/usr/bin/env python

import rospy 
from std_msgs.msg import Float64MultiArray
from std_msgs.msg import Float64
from geometry_msgs.msg import PoseStamped


def callback(data):
    print("working")
    print(data)

def listener():
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("results_array", Float64MultiArray , callback)

    rospy.spin()

if __name__ == '__main__':
    listener()