#!/usr/bin/env python3
"""
Framework   : OpenCV Aruco
Description : Calibration of camera and using that for finding pose of multiple markers
Status      : Working
References  :
    1) https://docs.opencv.org/3.4.0/d5/dae/tutorial_aruco_detection.html
    2) https://docs.opencv.org/3.4.3/dc/dbb/tutorial_py_calibration.html
    3) https://docs.opencv.org/3.1.0/d5/dae/tutorial_aruco_detection.html
"""

from math import floor
import numpy as np
import time

from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from sensor_msgs.msg import CameraInfo
from sensor_msgs.msg import Imu
import tf
from std_msgs.msg import UInt32
from std_msgs.msg import String
import message_filters
import tf.transformations as tr
import numpy as np
import pickle
import glob
import cv2
import cv2.aruco as aruco


CALIB_PATH_PARAM = '/home/makeruser/wifi-Project/Aruco_Tracker/images/for_calib/*.jpg'  #change those images and location
ARUCO_DICT_PARAM = aruco.DICT_4X4_250 #this work for https://chev.me/arucogen/
MARKER_LENGTH_METER = 0.19 # meters

VIDEO_PATH_INDEX = 1
OUTPUT_FILE_INDEX = 2
ROOM_NUMBER_INDEX = 3
HUMAN_IDS_INDEX = 4
FLOOR_IDS_INDEX = 5


FLOOR_IDS = [102, 103, 104]
HUMAN_IDS = [0, 101, 1, 100]


def get_position_from_single_aruco(rvec, tvec, ids):
    # draw axis for the aruco markers
    rot_mat_obj2cam, _ = cv2.Rodrigues(rvec)
    rot_mat_cam2obj = rot_mat_obj2cam.T  # transpose the object-to-cam rotation matrix to get cam-to-object
    # add padding to the rotation matrix to get dim(4,4)
    rot_mat_cam2obj_padded = np.zeros((4, 4))
    rot_mat_cam2obj_padded[:3, :3] = rot_mat_cam2obj
    rot_mat_cam2obj_padded[3, 3] = 1

    quat=tr.quaternion_from_matrix(rot_mat_cam2obj_padded) #obtain the cam-to-object quaternion rotation indices

    # translate = np.dot(rot_mat_cam2obj, tvec[0])  # rotate the translation vector
    translate = np.dot(-1 * rot_mat_cam2obj, tvec[0])  # rotate the translation vector

    # if(translate[0] > 0):
    #     br.sendTransform((translate),(quat),rospy.Time.now(),"cam_loc_"+ str(ids[0]),"aruco_"+str(ids[0])) #publish the transformation for this tag
    # else:
    #     pass

    return translate

def save_load_calib(mtx=None, dist=None, save_calib=False):
    """saves  the calibration files if they are not exits or load the calibration files if they do exist"""
    if save_calib and mtx is not None and dist is not None:
        import pickle
        with open('calib_mtx.pkl', 'wb') as f:
            pickle.dump(mtx, f)
        with open('calib_dist.pkl', 'wb') as f:
            pickle.dump(dist, f)

    if mtx is None or dist is None:
        import pickle
        with open('calib_mtx.pkl', 'rb') as f:
            mtx = pickle.load(f)
        with open('calib_dist.pkl', 'rb') as f:
            dist = pickle.load(f)

    return mtx, dist

def get_position_from_image(frame, to_draw=False, to_show=False, mtx=None, dist=None, save_calib=False):

    mtx, dist = save_load_calib(mtx=mtx, dist=dist, save_calib=save_calib)
    #print(mtx, dist)
    # operations on the frame
    # import pdb
    # pdb.set_trace()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # set dictionary size depending on the aruco marker selected
    aruco_dict = aruco.Dictionary_get(ARUCO_DICT_PARAM)

    # detector parameters can be set here (List of detection parameters[3])
    parameters = aruco.DetectorParameters_create()
    parameters.adaptiveThreshConstant = 10

    # lists of ids and the corners belonging to each id
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    # font for displaying text (below)app
    font = cv2.FONT_HERSHEY_SIMPLEX

    # check if the ids list is not empty
    # if no check is added the code will crash
    positions = []
    if np.all(ids != None):
        # estimate pose of each marker and return the values
        # rvet and tvec-different from camera coefficients
        rvec, tvec , rel_corners = aruco.estimatePoseSingleMarkers(corners, MARKER_LENGTH_METER, mtx, dist)
        #(rvec-tvec).any() # get rid of that nasty numpy value array error
        for i in range(0, ids.size):
            if(ids[i] in FLOOR_IDS):    # floor ids
                pos = get_position_from_single_aruco(rvec[i], tvec[i], ids[i])
                #print(ids[i], pos)
                print( tvec[i], rvec[i])
                # time.sleep(0.5)

            elif(ids[i] in HUMAN_IDS):   #human ids -> without transpose
                # pos = get_human_position_from_single_aruco(rvec[i], tvec[i], ids[i])
                pass
            else:   #unknown ids -> same as floor ids
                pos = get_position_from_single_aruco(rvec[i], tvec[i], ids[i])

            positions.append([ids[i], pos])

            if to_draw:
                aruco.drawAxis(frame, mtx, dist, rvec[i], tvec[i], 0.1)
        if to_draw:
            # draw a square around the markers
            aruco.drawDetectedMarkers(frame, corners)

            # code to show ids of the marker found
            strg = ''
            y0 , dy= 32, 25

            for i in range(0, ids.size):
                if(ids[i] in FLOOR_IDS):
                    strg += str(ids[i][0])+': Floor ' + '[{:.2f}, {:.2f}, {:.2f}]\n'.format(positions[i][1][0], positions[i][1][1], positions[i][1][2])
                elif(ids[i] in HUMAN_IDS):
                    strg += str(ids[i][0])+': Human ' + '[{:.2f}, {:.2f}, {:.2f}]\n'.format(positions[i][1][0], positions[i][1][1], positions[i][1][2])
                else:
                    strg += str(ids[i][0])+': Undefined ' + '[{:.2f}, {:.2f}, {:.2f}]\n'.format(positions[i][1][0], positions[i][1][1], positions[i][1][2])

            # an calculatioin to display all the id's properly on the screen 
            for x, line in enumerate(strg.split('\n')[:-1]):
                y = y0 + x*dy
                cv2.putText(frame, "Id " + line, (0, y), font, 0.6, (0, 255, 0), 2, cv2.LINE_AA)
    else:
        if to_draw:
            # code to show 'No Ids' when no markers are found
            cv2.putText(frame, "No Ids", (0, 32), font, 0.8, (0,255,0), 2, cv2.LINE_AA)
    # display the resulting frame
    if to_show:
        cv2.imshow('frame', frame)
        cv2.waitKey(1)
        #if cv2.waitKey(1) & 0xFF == ord('q'):
        #    break
    return positions


def get_position_from_video(cap, to_draw=False, to_show=False, mtx=None, dist=None, save_calib=False):
    # ------------- ARUCO TRACKER ---------------------------
    ret, frame = cap.read()
    frame = cv2.rotate(frame, cv2.cv2.ROTATE_180)
    #print(ret)
    positions = get_position_from_image(frame, to_draw=to_draw, to_show=to_show, mtx=mtx, dist=dist, save_calib=save_calib)
    return positions


if __name__ == '__main__':


    video = 0

    cap = cv2.VideoCapture(video)  # vapturing from the video, video - selcted by the user.
   
    while(True):
        positions = get_position_from_video(cap, to_draw=True, to_show=True)

        # for pos in positions:
        #     if pos[0][0] in FLOOR_IDS:    # recognized as a floor id's  
        #         print('{}: Floor [{:.2f}, {:.2f}, {:.2f}]'.format(pos[0][0], pos[1][0], pos[1][1], pos[1][2]))    
        #     elif pos[0][0] in HUMAN_IDS:    # recognized as a human id's 
        #         print('{}: Human [{:.2f}, {:.2f}, {:.2f}]'.format(pos[0][0], pos[1][0], pos[1][1], pos[1][2]))
        #     else:   # recognized id but undefined id
        #         print('{}: Undefined [{:.2f}, {:.2f}, {:.2f}]'.format(pos[0][0], pos[1][0], pos[1][1], pos[1][2]))

    cap.release()
    cv2.destroyAllWindows()
