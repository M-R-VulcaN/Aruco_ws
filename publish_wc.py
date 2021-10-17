#!/usr/bin/python

import rospy
import tf2_ros
import geometry_msgs.msg
from geometry_msgs.msg import PoseStamped
from math import pi, isinf
import numpy as np
from std_msgs.msg import Float64MultiArray
from std_msgs.msg import Float64

import time

import tf_conversions
from tf.transformations import euler_from_quaternion, quaternion_from_euler, quaternion_multiply
import yaml
import sys

results_filtered=0

FLOOR_IDS_INDEX = 1
CAMERA_LOC_INDEX = 2

if len(sys.argv) == 1:
    FLOOR_IDS = [102,103,104]
else:
    floor_ids_str = sys.argv[FLOOR_IDS_INDEX]
    FLOOR_IDS = floor_ids_str.split(',')
    FLOOR_IDS = [int(i) for i in FLOOR_IDS]

    camera_location = sys.argv[CAMERA_LOC_INDEX]
    camera_location = np.fromstring(camera_location.strip('[').strip(']'), sep=',')
    print(camera_location)

    
if __name__ == '__main__':
    rospy.init_node('publish_wc', anonymous=False)
    pub = rospy.Publisher('results_array', Float64MultiArray, queue_size=10)
    rel_pub = rospy.Publisher('aruco_localization_reliability', Float64, queue_size=1)
    pose_pub = rospy.Publisher("aruco_ground_truth", PoseStamped, queue_size=1)
    tfBuffer = tf2_ros.Buffer()
    listener = tf2_ros.TransformListener(tfBuffer)

    br = tf2_ros.TransformBroadcaster()

    r=rospy.Rate(40)

    num_of_markers = len(FLOOR_IDS)

    results=np.zeros((num_of_markers,6))

    last_translation = np.zeros((num_of_markers,3))

    #starting a timer
    start_time = time.time()

    while not rospy.is_shutdown():
        r.sleep()
        results=np.zeros((1,6))
        weighted_sum = np.array(0.0)
        
        for num in FLOOR_IDS:    
            try:

                transform_lc = tfBuffer.lookup_transform("cam_loc_"+str(num),"aruco_"+str(num), rospy.Time(0))

                x=transform_lc.transform.translation.x
                y=transform_lc.transform.translation.y
                z=transform_lc.transform.translation.z
                

            except Exception as e:
                # rospy.loginfo(e)
                continue

            curr_translation=np.array((x,y,z))

            distance = np.linalg.norm(curr_translation)
            weight = 1 # / distance    #TEMP - EACH WEIGHT IS EQUAL

            try: 
                transform_wc = tfBuffer.lookup_transform("room_link", "cam_loc_"+str(num), rospy.Time(0))
                qx = transform_wc.transform.rotation.x
                qy = transform_wc.transform.rotation.y
                qz = transform_wc.transform.rotation.z
                qw = transform_wc.transform.rotation.w
                x=transform_wc.transform.translation.x
                y=transform_wc.transform.translation.y
                z=transform_wc.transform.translation.z
                (roll, pitch, yaw) = euler_from_quaternion ([qx,qy,qz,qw],axes='sxyz')
                #print("Aruco " + str(num) + " roll = " + str(roll) +" pitch = " + str(pitch) + " yaw = " + str(yaw) + " x = " + str(x) + " y = " + str(y) + " z = " + str(z))
                # rospy.loginfo("Aruco 10%i roll= %f  pitch = %f  yaw = %f x=%f y=%f z=%f",num,roll,pitch,yaw,x,y,z )

                cam = camera_location
                # cam = np.array(camera_location)
                dist = np.linalg.norm(cam - np.array([x,y,z]))
                print('dist of id {} is {}'.format(str(num), str(dist)))
                if dist < 1.0:
                    results += weight*np.array([x,y,z,roll,pitch,yaw])

                    weighted_sum += weight
                # print(num," ==> ", np.array([x,y,z,roll,pitch,yaw]))
            except Exception as e:
                rospy.loginfo(e)
                continue

        if weighted_sum != 0:
            results = results / weighted_sum
            results = results.flatten()

            # if the timer > 35 seconds  -> results_filtered = results_filtered_last
            if(start_time + 35 > time.time()):
                results_filtered=results_filtered*0.98+results*0.02
                last_results_filtered = results_filtered
            else:
                results_filtered = last_results_filtered

            data_to_publish = Float64MultiArray()  # the data to be sent, initialise the array
            data_to_publish.data = results#.flatten() # assign the array with the value you want to send
            pub.publish(data_to_publish)

            t = geometry_msgs.msg.TransformStamped()
            t.header.stamp = rospy.Time.now()
            t.header.frame_id = "room_link"
            t.child_frame_id = "cam_weighted"
            t.transform.translation.x = results_filtered[0]
            t.transform.translation.y = results_filtered[1]
            t.transform.translation.z = results_filtered[2]
            
            q = tf_conversions.transformations.quaternion_from_euler(results_filtered[3],results_filtered[4],results_filtered[5])
            t.transform.rotation.x = q[0]
            t.transform.rotation.y = q[1]
            t.transform.rotation.z = q[2]
            t.transform.rotation.w = q[3]
            #print(t)
            br.sendTransform(t)

            factor = 1 #transform weighted sum into stdev
            reliability=Float64()
            reliability.data = weighted_sum * factor 
            rel_pub.publish(reliability)
