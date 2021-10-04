#!/bin/bash

#this is the folder that contains the files:
# /home/makeruser/Desktop/record-wifi-results/

source ~/Aruco_ws/devel/setup.bash

FOLDER_NAME = '/home/makeruser/Desktop/record-wifi-results'

# input 1 -> room_1_...... ->/room_1_../params.yaml
# patamsYamlToLaunch.py -> /home/makeruser/Aruco_ws/src/aruco_tf/src/launch

# python2.7 paramsYamlToLaunch.py $1
python2.7 paramsYamlToLaunch.py $FOLDER_NAME +'/room_'+$1+'/params.yaml'

sleep .5

gnome-terminal --tab --title="roslaunch" -- roslaunch aruco_tf room_$1.launch

sleep 2.5
 
# gnome-terminal --tab --title="publish_ws" -- python2.7 /usr/local/bin/scripts_raw_data_to_dataset/publish_wc.py
gnome-terminal --tab --title="publish_ws" -- python2.7 /home/makeruser/Aruco_ws/publish_wc.py

sleep 5

# gnome-terminal --tab --title="aruco" -- python2.7 /usr/local/bin/scripts_raw_data_to_dataset/ArucoDetectRos.py video.mp4 room_$1_aruco.csv #~/Aruco_ws/src/aruco_tf/src/src/ArucoDetectRos.py video.mp4 room_$1_aruco.csv

# input 1 -> room_1_...... -> /room_1_../ video.mp4
# output-> ~/temp/aruco_outputs/room_1_aruco.csv
# gnome-terminal --tab --title="aruco" -- python2.7 /home/makeruser/Aruco_ws/src/aruco_tf/src/src/ArucoDetectRos.py video.mp4 room_$1_aruco.csv
gnome-terminal --tab --title="aruco" -- python2.7 /home/makeruser/Aruco_ws/src/aruco_tf/src/src/ArucoDetectRos.py  $FOLDER_NAME + '/room_'+$1+'/video.mp4'
