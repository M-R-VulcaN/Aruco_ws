# !/bin/bash

source ~/Aruco_ws/devel/setup.bash

#defines- folders and Aruco ids.
SCRIPTS_PATH="/home/makeruser/Aruco_ws/src/aruco_tf/src/src"
LAUNCH_FILE_PATH="/home/makeruser/Aruco_ws/src/aruco_tf/src/launch"
RESULTS_FOLDER_PATH="/home/makeruser/Desktop/record-wifi-results"
TEMP_FOLDER_PATH="/home/makeruser/temp"

# FLOOR_ARUCO_IDS=(102,103,104)
# HUMAN_ARUCO_IDS=(0,1,100,101)
echo "creating launch file..."
python2.7 paramsYamlToLaunch.py  "$RESULTS_FOLDER_PATH/room_$1/params.yaml"   $1   "$LAUNCH_FILE_PATH"
sleep .5

echo "running the launch file..."
gnome-terminal --tab --title="roslaunch" -- roslaunch aruco_tf room_$1.launch

sleep 2.5
echo "running publish_ws..."
gnome-terminal --tab --title="publish_ws" -- python2.7 /home/makeruser/Aruco_ws/publish_wc.py   #${FLOOR_ARUCO_IDS}

sleep .5
echo "running the ArucoDetectRos..."
python2.7 /home/makeruser/Aruco_ws/src/aruco_tf/src/src/ArucoDetectRos.py  "$RESULTS_FOLDER_PATH/room_$1/video.mp4"   "$TEMP_FOLDER_PATH/aruco_outputs"   $1   #${HUMAN_ARUCO_IDS}   ${FLOOR_ARUCO_IDS}
echo "finished Aruco and generated csv file of the aruco"

echo "adding labels to Aruco csv..."
python3 /home/makeruser/Aruco_ws/src/aruco_tf/src/src/fromLablesToData.py "$TEMP_FOLDER_PATH/labels_files/room_$1_labels.csv"   "$TEMP_FOLDER_PATH/aruco_outputs/room_$1_aruco.csv"   "$TEMP_FOLDER_PATH/room_output/room_$1.csv"
echo "finished adding labels"

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