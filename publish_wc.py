#!/usr/bin/python

# sucscribes to log_ranges and publishes PointStanmed message in LC
# if transformation between 'drone' and 'world' exists, publishes PointStamped message in WC
# publishes laserscan in 'drone' frame, and converts it to PointCloud2 too.


import rospy
import tf2_ros
import geometry_msgs.msg
from geometry_msgs.msg import PoseStamped
from math import pi, isinf
import numpy as np
from std_msgs.msg import Float64MultiArray
from std_msgs.msg import Float64

import tf_conversions
from tf.transformations import euler_from_quaternion, quaternion_from_euler, quaternion_multiply

if __name__ == '__main__':
    rospy.init_node('publish_wc', anonymous=False)
    pub = rospy.Publisher('results_array', Float64MultiArray, queue_size=10)
    rel_pub = rospy.Publisher('aruco_localization_reliability', Float64, queue_size=1)
    pose_pub = rospy.Publisher("aruco_ground_truth", PoseStamped, queue_size=1)
    tfBuffer = tf2_ros.Buffer()
    listener = tf2_ros.TransformListener(tfBuffer)

    br = tf2_ros.TransformBroadcaster()

    r=rospy.Rate(100)

    num_of_markers=69
    #results=np.zeros((num_of_markers,6))

    last_translation = np.zeros((num_of_markers+1,3))

    while not rospy.is_shutdown():
        r.sleep()
        results=np.zeros((1,6))
        weighted_sum = np.array(0.0)
        for num in range(num_of_markers):
            try:
                transform_lc = tfBuffer.lookup_transform("loc_"+str(num),"aruco_"+str(num), rospy.Time(0))
                x=transform_lc.transform.translation.x
                y=transform_lc.transform.translation.y
                z=transform_lc.transform.translation.z
            except Exception as e:
                #rospy.loginfo(e)
                continue
            
            curr_translation=np.array((x,y,z))

            if np.array_equal(last_translation[num],curr_translation):
                continue

            # print (curr_translation , "  " , last_translation[num])

            last_translation[num]=curr_translation
            distance = np.linalg.norm(curr_translation)
            weight = 1 / distance
            # print("dist = " , distance ,"weight = ", weight)


            transform_wc = tfBuffer.lookup_transform("world", "loc_"+str(num), rospy.Time(0))
            qx = transform_wc.transform.rotation.x
            qy = transform_wc.transform.rotation.y
            qz = transform_wc.transform.rotation.z
            qw = transform_wc.transform.rotation.w
            x=transform_wc.transform.translation.x
            y=transform_wc.transform.translation.y
            z=transform_wc.transform.translation.z
            (roll, pitch, yaw) = euler_from_quaternion ([qx,qy,qz,qw],axes='sxyz')
            # rospy.loginfo("marker# %i roll= %f  pitch = %f  yaw = %f x=%f y=%f z=%f",num,roll,pitch,yaw,x,y,z )
            results += weight*np.array([x,y,z,roll,pitch,yaw])
            weighted_sum += weight
            # print(num," ==> ", np.array([x,y,z,roll,pitch,yaw]))
        
        #print("1)",results)
        if weighted_sum != 0:
            results = results / weighted_sum
            results = results.flatten()
            data_to_publish = Float64MultiArray()  # the data to be sent, initialise the array
            data_to_publish.data = results#.flatten() # assign the array with the value you want to send
            #print("2)" , data_to_publish)
            pub.publish(data_to_publish)

            t = geometry_msgs.msg.TransformStamped()
            t.header.stamp = rospy.Time.now()
            t.header.frame_id = "world"
            t.child_frame_id = "ground_truth_aruco"
            t.transform.translation.x = results[0]
            t.transform.translation.y = results[1]
            t.transform.translation.z = results[2]
            q = tf_conversions.transformations.quaternion_from_euler(results[3],results[4],results[5]+1.57)
            
            t.transform.rotation.x = q[0]
            t.transform.rotation.y = q[1]
            t.transform.rotation.z = q[2]
            t.transform.rotation.w = q[3]
            br.sendTransform(t)

            factor = 1 #transform weighted sum into stdev
            reliability=Float64()
            reliability.data = weighted_sum * factor 
            rel_pub.publish(reliability)

            pose = PoseStamped()
            pose.header.stamp = rospy.Time.now()
            pose.header.frame_id = "world"
            pose.pose.position.x = results[0]
            pose.pose.position.y = results[1]
            pose.pose.position.z = results[2]
            pose.pose.orientation.x = q[0]
            pose.pose.orientation.y = q[1]
            pose.pose.orientation.z = q[2]
            pose.pose.orientation.w = q[3]
            pose_pub.publish(pose)
