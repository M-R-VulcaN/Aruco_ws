# !/bin/bash

source ~/Aruco_ws/devel/setup.bash

#--------------------FOLDERS AND ARUCO IDS-------------------------------
SCRIPTS_PATH="/home/makeruser/Aruco_ws/src/aruco_tf/src/src"
LAUNCH_FILE_PATH="/home/makeruser/Aruco_ws/src/aruco_tf/src/launch"
RESULTS_FOLDER_PATH="/home/makeruser/Desktop/record-wifi-results"
# 
BASELINE_FOLDER_PATH="/home/makeruser/Desktop/baseline"
TEMP_FOLDER_PATH="/home/makeruser/temp"

FLOOR_ARUCO_IDS=(102,103,104)
HUMAN_ARUCO_IDS=(0,1,100,101)
#------------------------------------------------------------------------

echo "used Aruco:"
echo "floor ids: ${FLOOR_ARUCO_IDS[@]}"
echo "human ids: ${HUMAN_ARUCO_IDS[@]}"

echo "creating launch file..."
declare -a CAMERA_LOCATION

# #go to this file and change "qr102,qr103,qr104" to the aruco ids that you wrote to the yaml file.
# CAMERA_LOCATION=($(python2.7 paramsYamlToLaunch.py  "$RESULTS_FOLDER_PATH/room_$1/params.yaml"   $1   "$LAUNCH_FILE_PATH"  2>&1 > /dev/null))
# echo "done!"
# echo "camera location: ${CAMERA_LOCATION[@]}"
# sleep 0.5

# declare -a CAM=(${CAMERA_LOCATION[0]},${CAMERA_LOCATION[1]},${CAMERA_LOCATION[2]})

# echo "running the launch file..."
# gnome-terminal --tab --title="roslaunch" -- roslaunch aruco_tf room_$1.launch

# # sleep 2.5
# # gnome-terminal --tab --title="rviz" -- rosrun rviz rviz -d /home/makeruser/Desktop/aruco_cfg.rviz

# echo "running publish_ws..."
# gnome-terminal --tab --title="publish_ws" -- python2.7 /home/makeruser/Aruco_ws/publish_wc.py   ${FLOOR_ARUCO_IDS[@]}   $CAM

# sleep .5
# echo "running the ArucoDetectRos..."
# python2.7 /home/makeruser/Aruco_ws/src/aruco_tf/src/src/ArucoDetectRos.py  "$RESULTS_FOLDER_PATH/room_$1/video.mp4"   "$TEMP_FOLDER_PATH/aruco_outputs"   $1   ${HUMAN_ARUCO_IDS[@]}   ${FLOOR_ARUCO_IDS[@]}
# echo "finished Aruco and generated csv file of the aruco"

# echo "closing all unnecessary terminal tabs: PIDs: $(pgrep bash)"
# sleep .5
# kill $(pgrep gnome-terminal)
# sleep .5

# gnome-terminal --tab --title="roskill" -- killall -9 roscore && killall -9 rosmaster

# echo "adding labels to Aruco csv..."
# python3 /home/makeruser/Aruco_ws/src/aruco_tf/src/src/fromLablesToData.py "$TEMP_FOLDER_PATH/labels_files/room_$1_labels.csv"   "$TEMP_FOLDER_PATH/aruco_outputs/room_$1_aruco.csv"   "$TEMP_FOLDER_PATH/room_output/room_$1.csv"
echo "finished adding labels"

out=`python3 $SCRIPTS_PATH/pcapFolders.py  "$RESULTS_FOLDER_PATH/room_$1"`
out=`python3 $SCRIPTS_PATH/pcapFolders.py  "$BASELINE_FOLDER_PATH/room_$1"`

IFS=$'\n'; out_array=($out); unset IFS;
dir_counter=0
for dir in "${out_array[@]}"
do
	echo  $dir
    echo "pcap index: $dir_counter"
    echo "-------------------------"
#in case you are working on movement pcap:
    python3 /home/makeruser/Aruco_ws/src/aruco_tf/src/src/pcapToCsv.py   $1   $dir    "$TEMP_FOLDER_PATH/room_output/room_$1.csv"  $dir_counter
#in case you are working on baseline pcap:
    # python3 /home/makeruser/Aruco_ws/src/aruco_tf/src/src/pcapCsv.py   $1   $dir    "$BASELINE_FOLDER_PATH/room_output/room_$1.csv"  $dir_counter
    let dir_counter++
done