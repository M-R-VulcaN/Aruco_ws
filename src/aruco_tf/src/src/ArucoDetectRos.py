#!/usr/bin/env python3
from __future__ import division  #in order to be able to set the (1/30)
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
import rospy
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
import csv
import tf2_ros
import easygui
import sys

CALIB_PATH_PARAM = '/home/makeruser/wifi-Project/Aruco_Tracker/images/for_calib/*.jpg'  #change those images and location
ARUCO_DICT_PARAM = aruco.DICT_4X4_250 #this work for https://chev.me/arucogen/
MARKER_LENGTH_METER = 0.19 # meters

VIDEO_PATH_INDEX = 1
OUTPUT_FILE_INDEX = 2
ROOM_NUMBER_INDEX = 3
HUMAN_IDS_INDEX = 4
FLOOR_IDS_INDEX = 5


if len(sys.argv) == 1:
    FLOOR_IDS = [102, 103, 104]
    HUMAN_IDS = [0, 101, 1, 100]
else:
    floor_ids_str = sys.argv[FLOOR_IDS_INDEX]
    FLOOR_IDS = floor_ids_str.split(',')
    FLOOR_IDS = [int(i) for i in FLOOR_IDS]

    human_ids_str = sys.argv[HUMAN_IDS_INDEX]
    HUMAN_IDS = human_ids_str.split(',')
    HUMAN_IDS = [int(i) for i in HUMAN_IDS]


def calib_camera(calib_path=CALIB_PATH_PARAM):
    """Callibration"""
    # termination criteria for the iterative algorithm
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    # checkerboard of size (7 x 6) is used
    objp = np.zeros((9*9, 3), np.float32)
    objp[:,:2] = np.mgrid[0:9, 0:9].T.reshape(-1, 2)

    # arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.

    # iterating through all calibration images
    # in the folder

    images = glob.glob(calib_path)
    counter = 0
    for fname in images:
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        # find the chess board (calibration pattern) corners
        ret, corners = cv2.findChessboardCorners(gray, (9, 9), None)

        # if calibration pattern is found, add object points,
        # image points (after refining them)
        if ret == True:
            print(fname.split('/')[-1])
            counter += 1
            objpoints.append(objp)

            # Refine the corners of the detected corners
            corners2 = cv2.cornerSubPix(gray,corners,(11, 11),(-1, -1), criteria)
            imgpoints.append(corners2)

            # Draw and display the corners
            img = cv2.drawChessboardCorners(img, (9, 9), corners2, ret)
            cv2.imshow('img', img)
            cv2.waitKey(500)
    
    print(counter)      
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)
    print(mtx) 
    print(dist)
    # import pdb
    # pdb.set_trace()
    return ret, mtx, dist, rvecs, tvecs

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

    if(translate[0] > 0):
        br.sendTransform((translate),(quat),rospy.Time.now(),"cam_loc_"+ str(ids[0]),"aruco_"+str(ids[0])) #publish the transformation for this tag
    else:
        pass

    return translate

def get_human_position_from_single_aruco(rvec, tvec, ids): #without transposing
    # draw axis for the aruco markers

    rot_mat_obj2cam, _ = cv2.Rodrigues(rvec)
    rot_mat_cam2obj = rot_mat_obj2cam  # transpose the object-to-cam rotation matrix to get cam-to-object  //REMOVED .T
    # add padding to the rotation matrix to get dim(4,4)
    rot_mat_cam2obj_padded = np.zeros((4, 4))
    rot_mat_cam2obj_padded[:3, :3] = rot_mat_cam2obj
    rot_mat_cam2obj_padded[3, 3] = 1
    
    quat=tr.quaternion_from_matrix(rot_mat_cam2obj_padded) #obtain the cam-to-object quaternion rotation indices
    
    translate = tvec[0] #np.dot( rot_mat_cam2obj, tvec[0])  # rotate the translation vector
    # print('person is at {:.2f},{:.2f},{:.2f}'.format(translate[0],translate[1],translate[2]))
    br.sendTransform((translate),(quat),rospy.Time.now(),"human_loc_"+ str(ids[0]),"cam_weighted") #publish the transformation for this tag
    time.sleep(0.001)
    #print('{:.2f}, {:.2f}, {:.2f}'.format(translate[0], translate[1], translate[2]))
    try:
        transform_wc = tfBuffer.lookup_transform("cam_weighted", "human_loc_"+str(ids[0]), rospy.Time())
        xwc=transform_wc.transform.translation.x
        ywc=transform_wc.transform.translation.y
        zwc=transform_wc.transform.translation.z
        transform_wc = tfBuffer.lookup_transform("room_link", "human_loc_"+str(ids[0]), rospy.Time())
        x=transform_wc.transform.translation.x
        y=transform_wc.transform.translation.y
        z=transform_wc.transform.translation.z
        print('person (in camera link) is at {:.2f},{:.2f},{:.2f}'.format(xwc,ywc,zwc))
        return np.array((x,y,z))
    except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
        pass

    # transform_wc = tfBuffer.lookup_transform("room_link", "human_loc_"+str(ids[0]), rospy.Duration(1))
    # return np.array((x,y,z))
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
                #time.sleep(0.5)

            elif(ids[i] in HUMAN_IDS):   #human ids -> without transpose
                pos = get_human_position_from_single_aruco(rvec[i], tvec[i], ids[i])
            
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
    #time.sleep(0.03)
    #print(ret)
    positions = get_position_from_image(frame, to_draw=to_draw, to_show=to_show, mtx=mtx, dist=dist, save_calib=save_calib)
    return positions


def get_user_choise():
    room_number = sys.argv[ROOM_NUMBER_INDEX]
    # select = input("1 - Use Camera(usb port 0).\n2 - Use Recored Video\n\nSelect Your Choise: ")
    select = 2
    if(select == 1): # uses the camera as an input.
        video = 0
    elif(select == 2): #uses an already recoreded video.
        if len(sys.argv) == 1:
            video = easygui.fileopenbox(title='select video to detect arucos')
        else:
            video = sys.argv[VIDEO_PATH_INDEX]
            # '/home/makeruser/Desktop/record-wifi-results/room_'+room_number+'/video.mp4'
            # video = sys.argv[VIDEO_PATH_INDEX]
    else:  #wrong input - will cause a break.
        print("\n------\nerror! please select an option from the options above!\n------\n")
        return -1
    
    # creating and opening a csv file.
    # file_name = raw_input("\nPlase enter the .csv file name (enter room number only!): ")
    if len(sys.argv) == 1:
        file_name = easygui.filesavebox(title='select output file')
    else:
        # file_name = sys.argv[OUTPUT_FILE_INDEX]
        file_name = sys.argv[OUTPUT_FILE_INDEX]+'/room_' + str(room_number)+ '_aruco.csv'
    # file = open('room_'+file_name+'.csv','w')
    file = open(file_name,'w')
    
    return file,video


def time_stamp(count):
    # in order to create a user friendly time.
    count += 1/30   # because we were filming in 30 fps (1/30).

    hours = (count/60)/60
    minutes = count/60
    seconds = count % 60
    ms = count*1000

    timeCount = "%02d:%02d:%.3f" % (hours, minutes, seconds)
    return count,timeCount,ms


if __name__ == '__main__':


    #ret, mtx, dist, rvecs, tvecs = calib_camera()
    #save_load_calib(mtx=mtx, dist=dist, save_calib=True)
    #time.sleep(1000)
    count = 0
    frameCount = 0
    alreadywritten = False

    file,video = get_user_choise()

    writer = csv.writer(file)
    writer.writerow(['Time:','x','y','z','ms','Lable'])  #writing the first line to the csv file.

    rospy.init_node('arucoDetect')
    br = tf.TransformBroadcaster()
    time.sleep(1)
    tfBuffer = tf2_ros.Buffer()
    listener = tf2_ros.TransformListener(tfBuffer)
    
    cap = cv2.VideoCapture(video)  # vapturing from the video, video - selcted by the user.
    
    # ret, mtx, dist, rvecs, tvecs = calib_camera()
    
    while(True):
        positions = get_position_from_video(cap, to_draw=True, to_show=True)

        # continue ## AMIR -> added this to see prints

        count,timeCount,ms = time_stamp(count)  #creating a user friendly time and writing it to the csv.

        for pos in positions:
            if pos[0][0] in FLOOR_IDS:    # recognized as a floor id's  
                print('{}: Floor [{:.2f}, {:.2f}, {:.2f}]'.format(pos[0][0], pos[1][0], pos[1][1], pos[1][2]))
                
            elif pos[0][0] in HUMAN_IDS:    # recognized as a human id's 
                print('{}: Human [{:.2f}, {:.2f}, {:.2f}]'.format(pos[0][0], pos[1][0], pos[1][1], pos[1][2]))
                writer.writerow([timeCount, '{:.2f}'.format(abs(pos[1][0])),'{:.2f}'.format(abs(pos[1][1])),'{:.2f}'.format(abs(pos[1][2])),ms])
                                # ['Time:','x','y','z','ms']   >> writes to the csv file in this format.
                alreadywritten = True # setting it to prevent duplicates.
            else:   # recognized id but undefined id
                print('{}: Undefined [{:.2f}, {:.2f}, {:.2f}]'.format(pos[0][0], pos[1][0], pos[1][1], pos[1][2]))

        # in order to write the timestamp to the csv file even if non of the ids got recognized.
        # alreadywritten parameter should be false if human id NOT recognized.
        if(alreadywritten == False):
            writer.writerow([timeCount,'','','',ms]) # write the user friendly time to the csv file and ms.
        else:               #['Time:','x','y','z','ms']
            alreadywritten = False
        frameCount += 1

        print("-------------------------------")
        print("time: " + timeCount + "\n")
        print("video fps: ", frameCount/count)
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
