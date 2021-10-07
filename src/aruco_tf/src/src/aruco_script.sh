# !/bin/bash

#this is the folder that contains the files:
# /home/makeruser/Desktop/record-wifi-results/

source ~/Aruco_ws/devel/setup.bash
SCRIPTS_PATH="/home/makeruser/Aruco_ws/src/aruco_tf/src/src"
RESULTS_FOLDER_PATH="/home/makeruser/Desktop/record-wifi-results"
TEMP_FOLDER_PATH="/home/makeruser/temp"
# input 1 -> room_1_...... ->/room_1_../params.yaml
# patamsYamlToLaunch.py -> /home/makeruser/Aruco_ws/src/aruco_tf/src/launch
python2.7 paramsYamlToLaunch.py  "$RESULTS_FOLDER_PATH/room_$1/params.yaml"   $1
echo "finished creating a launch file."
sleep .5

echo "running the launch file"
gnome-terminal --tab --title="roslaunch" -- roslaunch aruco_tf room_$1.launch

sleep 2.5
echo "running publish_ws"
gnome-terminal --tab --title="publish_ws" -- python2.7 /home/makeruser/Aruco_ws/publish_wc.py

sleep .5
echo "running the ArucoDetectRos"
# input 1 -> room_1_...... -> /room_1_../ video.mp4
# output-> ~/temp/aruco_outputs/room_1_aruco.csv
python2.7 /home/makeruser/Aruco_ws/src/aruco_tf/src/src/ArucoDetectRos.py  "$RESULTS_FOLDER_PATH/room_$1/video.mp4"  $1
echo "finished Aruco and generated csv file of the aruco"

echo "adding labels to Aruco csv"
python3 /home/makeruser/Aruco_ws/src/aruco_tf/src/src/fromLablesToData.py "$TEMP_FOLDER_PATH/labels_files/room_$1_labels.csv"   "$TEMP_FOLDER_PATH/aruco_outputs/room_$1_aruco.csv"   "$TEMP_FOLDER_PATH/room_output/room_$1.csv"
echo "finished"

out=`python3 $SCRIPTS_PATH/pcapFolders.py  "$RESULTS_FOLDER_PATH/room_$1"`
# # run folders.py code
IFS=$'\n'; out_array=($out); unset IFS;
              
dir_counter=0
for dir in "${out_array[@]}"
do
	echo  $dir
    echo "pcap index: $dir_counter"
    python3 /home/makeruser/Aruco_ws/src/aruco_tf/src/src/pcapToCsv.py   $1   $dir    "$TEMP_FOLDER_PATH/room_output/room_$1.csv"  $dir_counter
    let dir_counter++
    # do something with each folder
done