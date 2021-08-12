#!/usr/bin/env python
import numpy as np
import time
import rospy
from cv_bridge import CvBridge
import cv2 as cv
import cv2.aruco as aruco
from sensor_msgs.msg import Image
from sensor_msgs.msg import CameraInfo
from sensor_msgs.msg import Imu
import tf
from std_msgs.msg import UInt32
from std_msgs.msg import String
import message_filters
import tf.transformations as tr


### USE CASE PARAMS
# CHANGE_USE_CASE = False
# CHANGE_USE_CASE_STRING = 'MODE_9_10FPS_1000'

### USE ARUCO PARAMS
aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_250)
markerLength = 0.19 # In meters
parameters = aruco.DetectorParameters_create()



class ArucoDetect():

    def __init__(self):
        self.bridge = CvBridge()

        # params for pico
        self.dist_coeffs = np.zeros(5)
        self.camera_matrix = np.eye(3)
        # self.camera_info_initialized = False
        
        #ID setup
        self.my_ids = [1,2,3,4]  #only these marker ids can be detected!

    def Detect(self,imgG):
        if self.camera_info_initialized==True:
            # blur = np.asarray(self.bridge.imgmsg_to_cv2(imgG,'mono16')).astype('uint16')
            # blur = (blur / np.single(blur.max()) * 255).astype('uint8') #convert to uint8 using max value 

            # blur = cv.erode(blur, cv.getStructuringElement(cv.MORPH_RECT, (5, 5)), iterations=1)
            # blur = cv.dilate(blur, cv.getStructuringElement(cv.MORPH_RECT, (7, 7)), iterations=1)
            # blur = cv.erode(blur, cv.getStructuringElement(cv.MORPH_RECT, (3, 3)), iterations=1)

            # blur = cv.medianBlur(blur, 9,9) # 11,11
            # blur = cv.equalizeHist(blur)

            corners, ids, rejectedImgPoints = aruco.detectMarkers(XXXXXXXXXXXXXXXXXXXXXXX, aruco_dict, parameters=parameters)
            rvec, tvec, _ = aruco.estimatePoseSingleMarkers(corners, markerLength, self.camera_matrix, self.dist_coeffs)
            blurShow = cv.cvtColor(XXXXXXXXXXXXXXXXXXXXXXX, cv.COLOR_GRAY2BGR) 


            if (type(ids) != type(None) and any(elem in self.my_ids  for elem in ids)):
                aruco.drawDetectedMarkers(blurShow, corners, ids , (255,0,0)) #for displaying the detected tags in rviz - includes ids not in my_ids list!
                #---
                for iii,id in enumerate(ids):
                    if id in self.my_ids:
                        # print("id: " + str(id[0]) + "  R1: " + str(rvec[iii][0][0]) + "  R2: " + str(rvec[iii][0][1]) +"  R3: " + str(rvec[iii][0][2]) + "  X: " + str(tvec[iii][0][0]) + "  Y: " + str(tvec[iii][0][1])  + "  Z: " + str(tvec[iii][0][2]) )
                        rot_mat_obj2cam , _ = cv.Rodrigues(rvec[iii])
                        rot_mat_cam2obj= rot_mat_obj2cam.T #transpose the object-to-cam rotation matrix to get cam-to-object

                        #add padding to the rotation matrix to get dim(4,4) 
                        rot_mat_cam2obj_padded=np.zeros((4,4)) 
                        rot_mat_cam2obj_padded[:3,:3]=rot_mat_cam2obj
                        rot_mat_cam2obj_padded[3,3]=1
                        
                        quat=tr.quaternion_from_matrix(rot_mat_cam2obj_padded) #obtain the cam-to-object quaternion rotation indices
                        translate=np.dot(-1*rot_mat_cam2obj,tvec[iii][0])                         #rotate the translation vector
                        br.sendTransform((translate),(quat),rospy.Time.now(),"loc_"+str(id[0]),"aruco_"+str(id[0])) #publish the transformation for this tag

            # img_pub = self.bridge.cv2_to_imgmsg(blurShow) #for displaying the detected tags in rviz
            # aruco_pub.publish(img_pub)
        else:
            print ("camera info not initialized")

    # def CamInfoCallBack(self,msg):
    #     if self.camera_info_initialized==False:
    #         self.dist_coeffs = msg.D
    #         self.camera_matrix = np.reshape(msg.K,(3,3))

    #         print('UPDATED CAMERA PROPERTIES')
    #         print (self.dist_coeffs)
    #         print (self.camera_matrix)
    #         self.camera_info_initialized=True

    #         if CHANGE_USE_CASE:
    #             UseCasePub.publish(CHANGE_USE_CASE_STRING)
    #             print('CHANGED USE_CASE TO ' + CHANGE_USE_CASE_STRING)

    #     else:
    #         return

if __name__ == '__main__':
    AD = ArucoDetect()
    rospy.init_node('arucoDetect')
    # UseCasePub = rospy.Publisher('use_case', String, queue_size=1,latch=True)

    time.sleep(1)
    # rospy.Subscriber("/left/camera_info", CameraInfo, AD.CamInfoCallBack)

    # rospy.Subscriber("/left/image_raw", Image, AD.Detect)
    br = tf.TransformBroadcaster()

    # aruco_pub = rospy.Publisher('aruco_stream_debug', Image, queue_size=1)
    #img_sub = message_filters.Subscriber("/royale_camera_driver/gray_image", Image)
    #imd_sub = message_filters.Subscriber("/royale_camera_driver/depth_image", Image)
    #ts = message_filters.TimeSynchronizer([img_sub, imd_sub], 1)
    #ts.registerCallback(AD.Detect)

    print("======= Calculate Aruco Node Initialized =======")
    rospy.spin()
    cv.destroyAllWindows()
