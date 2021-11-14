import os
import sys

PCAP_FILE_PATH_INDEX = 1
# ROOM_NUMBER = 2
# PCAP_FILE_NAME = 3
# PCAP_OUTPUT_FILE_NAME = 4

# directory = '/home/makeruser/Aruco_ws/src/aruco_tf/src/src/room_1/room_1_20210912-221555'
directory = sys.argv[PCAP_FILE_PATH_INDEX]

count = -1

for subdir, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith(".pcap"):
            count += 1
            print(str(subdir)+"/output.pcap")             
            continue
        else:
            continue
