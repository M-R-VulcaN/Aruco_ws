#!/usr/bin/env python

import rospy 
import tf2_msgs.msg
import geometry_msgs.msg

def callback(data):
    print("working")
    print(data)

def listener():
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("tf", tf2_msgs.msg.TFMessage , callback)

    rospy.spin()

if __name__ == '__main__':
    listener()