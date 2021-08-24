# Aruco_ws
**Ready dataset csv file for room 10:**
```
~/Aruco_ws/src/aruco_tf/src/src/ready dataset/room_10.csv
```
**Clone the repo to your computer**

**The code called ArucoDetectRos.py under the path Aruco_ws/src/aruco_tf/src/src/ArucoDetectRos.py**

**run:**
```
terminal 1: $ roscore

terminal 2: $ source ~/Aruco_ws/devel/setup.bash
            $ roslaunch aruco_tf static_new.launch

terminal 3: $ rviz
```

**RVIZ configuration:**
```
Add TF
change Global Frame > room_link
```

**use the client:**
```
run the client.py codeunder the path Aruco_ws/src/aruco_tf/client.py
```

**to display frame**
```
$ rosrun tf view_frames
$ evince frames.pdf 
```
