import os
import sys

PCAP_FILE_PATH_INDEX = 1
ROOM_NUMBER = 2
PCAP_FILE_NAME = 3
PCAP_OUTPUT_FILE_NAME = 4
# $PATH $1 output.pcap room_$1.csv


# directory = '/home/makeruser/Aruco_ws/src/aruco_tf/src/src/room_1/room_1_20210912-221555'
directory = sys.argv[PCAP_FILE_PATH_INDEX]

# print(directory) #Todo: Is this necessary?

count = -1

for subdir, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith(".pcap"):
            count += 1
            #do smth
            print(str(subdir)+"/output.pcap")
            # print(str(count) + "\n" + str(subdir)+"/output.pcap")
            # print(file + '     pcap:' + str(count) + "         " + subdir)
            # import pcapToCsv
             
            continue
        else:
            continue
