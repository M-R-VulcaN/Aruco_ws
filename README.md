# Aruco_ws

## _A dataset creator for wifi recording project_

[![N|Solid](https://thumbs.dreamstime.com/b/d-illustration-wifi-symbol-sign-internet-network-connection-background-wireless-187836855.jpg)](https://github.com/M-R-VulcaN/Record-Wifi)

developed by M-R-Vulcan Team

## <span style="color: yellow">Getting started:
- clone this repository
- cd ~/Aruco_ws/src/aruco_tf/src/src/
- pip3 install -r requirements.txt

## <span style="color: yellow">Run the bash script:
- ./aruco_script.sh < room number >

    for example: "<span style="color: red">./</span><span style="color: green">aruco_script.sh </span><span style="color: red">1</span>"

## <span style="color: yellow">aruco_script.sh:

- change the following parameters:

    #folder that contains the scripts from this repository:
    - <span style="color: green">SCRIPTS_PATH</span>="/home/USER/Aruco_ws/src/aruco_tf/src/src"  

    #folder that contains the launchfiles:
    - <span style="color: green">LAUNCH_FILE_PATH</span>="/home/USER/Aruco_ws/src/aruco_tf/src/launch"

    #folder that contains the recordings - with movement:
    - <span style="color: green">RESULTS_FOLDER_PATH</span>="/home/USER/recording-results/With_Movement/"

    #folder that contains the recordings - baseline:
    - <span style="color: green">BASELINE_FOLDER_PATH</span>="/home/USER/recording-results/Baseline/"

    #temporary folder
    - <span style="color: green">TEMP_FOLDER_PATH</span>="/home/USER/temp"

    #aruco ids that were used in the recording
    - <span style="color: green">FLOOR_ARUCO_IDS</span>=()
    - <span style="color: green">HUMAN_ARUCO_IDS</span>=()


## <span style="color: yellow">Display the csv files using Plotly:

- run the script <span style="color: green">"plot_data.py"</span>

**<span style="color: yellow">RVIZ Display configuration:**

- Add TF
- change Global Frame > room_link

**<span style="color: yellow">DatasetFix script:**

- after getting the csv files from aruco_script.sh its suggested to run "datasetFix.py".

    how to use:
    1. change the main_dir_path to the folder that contains all of the rooms(need to have a csv file called "dataset_room_X_pcap_X.csv" and a yaml file for the specific room)
    2. run the script(python3), enter the room number and pcap number of the specific '.csv' file. 
    3. the script will fix:
        * one place labels(for example: "walking", "walking", "sitting", "DO_NOT_USE" -> change "sitting"->"DO_NOT_USE")
        * replace all "DO_NOT_USE" labels to "Nan" -> changes the xyz to "Nan" as well, in most of the cases it solves the next step.
        * read the yaml file and return to the user all the points that are out of the room(if there are any).
        * replace all the points where the "z" is higher than 1.64 to "Nan" (usually happens in the ending of a movement)
        * creates a new csv file under the name of the csv that used and renames the used csv to _old.csv 


**<span style="color: yellow">Record ROS and display frames**

- $ rosrun tf view_frames
- $ evince frames.pdf 
