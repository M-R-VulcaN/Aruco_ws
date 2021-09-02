
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
results_filtered=0

human_ids = [0, 101, 1, 100]

if __name__ == '__main__':
    rospy.init_node('publish_wc', anonymous=False)
    pub = rospy.Publisher('results_array', Float64MultiArray, queue_size=10)
    rel_pub = rospy.Publisher('aruco_localization_reliability', Float64, queue_size=1)
    pose_pub = rospy.Publisher("aruco_ground_truth", PoseStamped, queue_size=1)
    tfBuffer = tf2_ros.Buffer()
    listener = tf2_ros.TransformListener(tfBuffer)

    br = tf2_ros.TransformBroadcaster()

    r=rospy.Rate(40)   # 100 Hz???????

    num_of_markers=3  # 102,103,104 
    results=np.zeros((num_of_markers,6))

    last_translation = np.zeros((num_of_markers+2,3))

    while not rospy.is_shutdown():
        r.sleep()
        results=np.zeros((1,6))
        weighted_sum = np.array(0.0)

        for num in range(2, num_of_markers+2):
            
            try:
                transform_lc = tfBuffer.lookup_transform("cam_loc_10"+str(num),"aruco_10"+str(num), rospy.Time(0))

                x=transform_lc.transform.translation.x
                y=transform_lc.transform.translation.y
                z=transform_lc.transform.translation.z

            except Exception as e:
                # rospy.loginfo(e)
                continue

            curr_translation=np.array((x,y,z))

            # #filtering that caused errors
            # if np.array_equal(last_translation[num],curr_translation):
            #     continue
            # print (curr_translation , "  " , last_translation[num])


            last_translation[num]=curr_translation
            distance = np.linalg.norm(curr_translation)
            weight = 1 # / distance    #TEMP - EACH WEIGHT IS EQUAL
            # print("dist = " , distance ,"weight = ", weight)
            # print("weight = " , weight)

            try: 
                transform_wc = tfBuffer.lookup_transform("room_link", "cam_loc_10"+str(num), rospy.Time(0))
                qx = transform_wc.transform.rotation.x
                qy = transform_wc.transform.rotation.y
                qz = transform_wc.transform.rotation.z
                qw = transform_wc.transform.rotation.w
                x=transform_wc.transform.translation.x
                y=transform_wc.transform.translation.y
                z=transform_wc.transform.translation.z
                (roll, pitch, yaw) = euler_from_quaternion ([qx,qy,qz,qw],axes='sxyz')
                print("Aruco 10" + str(num) + " roll = " + str(roll) +" pitch = " + str(pitch) + " yaw = " + str(yaw) + " x = " + str(x) + " y = " + str(y) + " z = " + str(z))
                # rospy.loginfo("Aruco 10%i roll= %f  pitch = %f  yaw = %f x=%f y=%f z=%f",num,roll,pitch,yaw,x,y,z )

                results += weight*np.array([x,y,z,roll,pitch,yaw])

                weighted_sum += weight
                # print(num," ==> ", np.array([x,y,z,roll,pitch,yaw]))
            except Exception as e:
                rospy.loginfo(e)
                continue

        # print("weighted_sum = "+ str(weighted_sum))
        if weighted_sum != 0:
            results = results / weighted_sum
            results = results.flatten()

            results_filtered=results_filtered*0.98+results*0.02
            # print("results_filtered = " +str(results_filtered))
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
            
            #here the error in the roll pitch yaw happens:
            q = tf_conversions.transformations.quaternion_from_euler(results_filtered[3],results_filtered[4],results_filtered[5])
            t.transform.rotation.x = q[0]
            t.transform.rotation.y = q[1]
            t.transform.rotation.z = q[2]
            t.transform.rotation.w = q[3]
            print(t)
            # print(t.transform.translation)
            br.sendTransform(t)

            factor = 1 #transform weighted sum into stdev
            reliability=Float64()
            reliability.data = weighted_sum * factor 
            rel_pub.publish(reliability)

        # for num in human_ids:
        #     try: 
        #         human_wc = tfBuffer.lookup_transform("room_link", "human_loc"+str(num), rospy.Time(0))
        #         qx = human_wc.transform.rotation.x
        #         qy = human_wc.transform.rotation.y
        #         qz = human_wc.transform.rotation.z
        #         qw = human_wc.transform.rotation.w
        #         x=human_wc.transform.translation.x
        #         y=human_wc.transform.translation.y
        #         z=human_wc.transform.translation.z

        #         t = geometry_msgs.msg.TransformStamped()
        #         t.header.stamp = rospy.Time.now()
        #         t.header.frame_id = "room_link"
        #         t.child_frame_id = "human_loc"
        #         t.transform.rotation.x = qx
        #         t.transform.rotation.y = qy
        #         t.transform.rotation.z = qz
        #         t.transform.rotation.w = qw
        #         t.transform.translation.x =x
        #         t.transform.translation.y = y
        #         t.transform.translation.z = z
        #         br.sendTransform(t)
        #     except Exception as e:
        #         rospy.loginfo(e)
        #     continue
           


