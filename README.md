# Aruco_ws
**Ready dataset csv file for room 10:**
```
ds_room_10.csv
```
**Clone the repo to your computer**

**The code called ArucoDetectRos.py under the path Aruco_ws/src/aruco_tf/src/src/ArucoDetectRos.py**

**run:**
```
$ source ~/Aruco_ws/devel/setup.bash
$ roslaunch aruco_tf static_new.launch
--------------------------------------
$ source ~/Aruco_ws/devel/setup.bash
$ cd ~/Aruco_ws/
$ python2.7 publish_ws.py
--------------------------------------
$ source ~/Aruco_ws/devel/setup.bash
$ cd ~/Aruco_ws/src/aruco_tf/src/src/
$ python2.7 ArucoDetectVideo.py
--------------------------------------
$ rviz
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
