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

calib_path_param = '/home/makeruser/wifi-Project/Aruco_Tracker/images/for_calib/*.jpg'  ########## AMIR -> change these images and location
aruco_dict_param = aruco.DICT_4X4_250 ########## AMIR -> this work for https://chev.me/arucogen/
marker_length = 0.19 # meters

# floor_ids = [101,102]
# human_ids = [100, 105]
floor_ids = [102, 103, 104]
human_ids = [0, 101, 1, 100]

####---------------------- CALIBRATION ---------------------------
def calib_camera(calib_path=calib_path_param):
    # termination criteria for the iterative algorithm
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    # checkerboard of size (7 x 6) is used
    objp = np.zeros((6*7, 3), np.float32)
    objp[:,:2] = np.mgrid[0:7, 0:6].T.reshape(-1, 2)

    # arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.

    # iterating through all calibration images
    # in the folder

    images = glob.glob(calib_path)

    for fname in images:
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        # find the chess board (calibration pattern) corners
        ret, corners = cv2.findChessboardCorners(gray, (7, 6), None)

        # if calibration pattern is found, add object points,
        # image points (after refining them)
        if ret == True:
            objpoints.append(objp)

            # Refine the corners of the detected corners
            corners2 = cv2.cornerSubPix(gray,corners,(11, 11),(-1, -1), criteria)
            imgpoints.append(corners2)

            # Draw and display the corners
            img = cv2.drawChessboardCorners(img, (7, 6), corners2, ret)


    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)
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

    translate = np.dot(-1 * rot_mat_cam2obj, tvec[0])  # rotate the translation vector

    br.sendTransform((translate),(quat),rospy.Time.now(),"cam_loc_"+ str(ids[0]),"aruco_"+str(ids[0])) #publish the transformation for this tag

    return translate

def get_my_position_from_single_aruco(rvec, tvec, ids):
    # draw axis for the aruco markers
    rot_mat_obj2cam, _ = cv2.Rodrigues(rvec)
    rot_mat_cam2obj = rot_mat_obj2cam  # transpose the object-to-cam rotation matrix to get cam-to-object  //REMOVED .T
    # add padding to the rotation matrix to get dim(4,4)
    rot_mat_cam2obj_padded = np.zeros((4, 4))
    rot_mat_cam2obj_padded[:3, :3] = rot_mat_cam2obj
    rot_mat_cam2obj_padded[3, 3] = 1
    
    quat=tr.quaternion_from_matrix(rot_mat_cam2obj_padded) #obtain the cam-to-object quaternion rotation indices
    
    translate = tvec[0] #np.dot( rot_mat_cam2obj, tvec[0])  # rotate the translation vector
    
    br.sendTransform((translate),(quat),rospy.Time.now(),"human_loc_"+ str(ids[0]),"cam_loc_"+str(floor_ids[0])) #publish the transformation for this tag

    #print('{:.2f}, {:.2f}, {:.2f}'.format(translate[0], translate[1], translate[2]))

    return translate

def save_load_calib(mtx=None, dist=None, save_calib=False):
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
    aruco_dict = aruco.Dictionary_get(aruco_dict_param)

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
        rvec, tvec , rel_corners = aruco.estimatePoseSingleMarkers(corners, marker_length, mtx, dist)
        #(rvec-tvec).any() # get rid of that nasty numpy value array error


        for i in range(0, ids.size):
            # floor ids
            if(ids[i] in floor_ids):
                pos = get_position_from_single_aruco(rvec[i], tvec[i], ids[i])
            #human ids -> without transpose
            elif(ids[i] in human_ids):
                pos = get_my_position_from_single_aruco(rvec[i], tvec[i], ids[i])
            #unknown ids -> same as floor ids
            else:
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
                if(ids[i] in floor_ids):
                    strg += str(ids[i][0])+': Floor ' + '[{:.2f}, {:.2f}, {:.2f}]\n'.format(positions[i][1][0], positions[i][1][1], positions[i][1][2])
                elif(ids[i] in human_ids):
                    strg += str(ids[i][0])+': Human ' + '[{:.2f}, {:.2f}, {:.2f}]\n'.format(positions[i][1][0], positions[i][1][1], positions[i][1][2])
                else:
                    strg += str(ids[i][0])+': Undefined ' + '[{:.2f}, {:.2f}, {:.2f}]\n'.format(positions[i][1][0], positions[i][1][1], positions[i][1][2])

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


    #ret, mtx, dist, rvecs, tvecs = calib_camera()
    #save_load_calib(mtx=mtx, dist=dist, save_calib=True)
    #time.sleep(1000)
    import csv
    file = open('testings10.csv','w')
    writer = csv.writer(file)

    writer.writerow(['Time:','Lable:','Aruco ID','x','y','z'])

    rospy.init_node('arucoDetect')
    br = tf.TransformBroadcaster()
    time.sleep(1)
    
    # cap = cv2.VideoCapture(0)
    test = raw_input("enter mp4 file name: ")
    print(test)
    cap = cv2.VideoCapture(test)

    count = 0
    frameCount = 0
    alreadywritten = False

    # ret, mtx, dist, rvecs, tvecs = calib_camera()
    while(True):
        positions = get_position_from_video(cap, to_draw=True, to_show=True)

        count += 0.033   # because we were filming in 30 fps (1/30)
        count = round(count, 3) #round the float number to only 3 digits after the 0 (x.xxx)
        
        hours = (count/60)/60
        minutes = count/60
        seconds = count % 60

        timeCount = "%02d:%02d:%.3f" % (hours, minutes, seconds)
        

        # writer.writerow(['{:.1f}'.format(timeElapsed)])
                            # ['Time:','Lable:','Aruco ID','x','y','z']   >> writes to the csv file in this format
        for pos in positions:
            if pos[0][0] in floor_ids:   
                print('{}: Floor [{:.2f}, {:.2f}, {:.2f}]'.format(pos[0][0], pos[1][0], pos[1][1], pos[1][2]))
                
            elif pos[0][0] in human_ids:
                print('{}: Human [{:.2f}, {:.2f}, {:.2f}]'.format(pos[0][0], pos[1][0], pos[1][1], pos[1][2]))
                writer.writerow([timeCount,'',pos[0][0],'{:.2f}'.format(pos[1][0]),'{:.2f}'.format(pos[1][1]),'{:.2f}'.format(pos[1][2])])
                                # ['Time:','Lable:','Aruco ID','x','y','z']   >> writes to the csv file in this format
                alreadywritten = True
            else:
                print('{}: Undefined [{:.2f}, {:.2f}, {:.2f}]'.format(pos[0][0], pos[1][0], pos[1][1], pos[1][2]))

        if(alreadywritten == False):
            writer.writerow([timeCount]) #write the time to the csv file
        else:
            alreadywritten = False

        frameCount += 1

        # writer.writerow(['{:.1f}'.format(timeElapsed)])
        print("-------------------------------")
        print("time: " + timeCount + "\n")
        print("frames: " , frameCount)

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
