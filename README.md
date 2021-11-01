# Aruco_ws

## _A dataset creator for wifi recording project_

[![N|Solid](https://thumbs.dreamstime.com/b/d-illustration-wifi-symbol-sign-internet-network-connection-background-wireless-187836855.jpg)](https://github.com/M-R-VulcaN/Record-Wifi)

developed by M-R-Vulcan Team

## How To Run:
- cd ~/Aruco_ws/src/aruco_tf/src/src/

and run the bash script:
- ./aruco_script.sh < room number >

for example:
./aruco_script.sh 1

## ./aruco_script.sh:
```
change the following parameters:

#folder that contains the scripts from this repository:
~SCRIPTS_PATH="/home/USER/Aruco_ws/src/aruco_tf/src/src"  

#folder that contains the launchfiles:
~LAUNCH_FILE_PATH="/home/USER/Aruco_ws/src/aruco_tf/src/launch"

#folder that contains the recordings - with movement:
~RESULTS_FOLDER_PATH="/home/USER/recording-results/With_Movement/"

#folder that contains the recordings - baseline:
~BASELINE_FOLDER_PATH="/home/USER/recording-results/Baseline/"

#temporary folder
~TEMP_FOLDER_PATH="/home/USER/temp"

#aruco ids that were used in the recording
~FLOOR_ARUCO_IDS=()
~HUMAN_ARUCO_IDS=()
```

**RVIZ configuration:**
```
Add TF
change Global Frame > room_link
```

**to record and display frames**
```
$ rosrun tf view_frames
$ evince frames.pdf 
```