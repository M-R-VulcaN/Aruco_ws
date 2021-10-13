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