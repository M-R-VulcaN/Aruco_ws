import sys
import numpy as np
import subprocess

room_numbers = [0,1,2,3,4,11,12,13,14]

for room in room_numbers:
    print("running bash script for room " + str(room))

    subprocess.call('xterm -e bash -c "/home/makeruser/Aruco_ws/src/aruco_tf/src/src/aruco_script.sh {}"'.format(int(room)), shell=True)
    
    print('done')
