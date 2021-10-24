"""
This code loads the pcap file and write its Timestamp and Data to the csv file 
and then importing the pcapFix.py script the sort the pcap data by its channels.
"""

import matplotlib.pyplot as plt
import numpy as np
import csv

from CSIKit.util.csitools import get_CSI
from CSIKit.util.filters import bandpass, hampel, running_mean
from CSIKit.reader import get_reader
import sys

import pandas as pd
import numpy as np

ROOM_NUMBER_INDEX = 1
PCAP_FILE_PATH_INDEX = 2
LABELED_ARUCO_FILE_PATH_INDEX = 3
PCAP_NUM_INDEX = 4

if len(sys.argv) == 1:
    ROOM_NUMBER = input("enter room number: ")
    PCAP_FILE_PATH = input("please enter PCAP file name: ")
    LABELED_ARUCO_FILE_PATH = "room_"+str(ROOM_NUMBER)+".csv"
    PCAP_NUM = str(0)
else:
    ROOM_NUMBER = sys.argv[ROOM_NUMBER_INDEX]
    PCAP_FILE_PATH = sys.argv[PCAP_FILE_PATH_INDEX]
    LABELED_ARUCO_FILE_PATH = sys.argv[LABELED_ARUCO_FILE_PATH_INDEX]
    PCAP_NUM = sys.argv[PCAP_NUM_INDEX]

if __name__ == "__main__":
    path: str=PCAP_FILE_PATH
    reader = get_reader(path)
    csi_data = reader.read_file(path)
    print ("csi_data.frames: ",len(csi_data.frames))
    finalEntry, no_frames, no_subcarriers = get_CSI(csi_data, metric=None, squeeze_output=True)
    print ("csi_data.timestamps: ",len(csi_data.timestamps))
    count = 0
    j = -1

    file_name = 'pcap_data.csv'
    with open(file_name, 'w') as csvfile:
        fieldnames = ['Timestamp', 'PC_time','pcapData']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        print("writing to file...")
        writer.writeheader()
        for i in csi_data.timestamps:
            j += 1
            pcTimer = i
            import time

            pcTimer = time.ctime(pcTimer)
            timer = (i - csi_data.timestamps[0])*1000 #in order to represent time in ms and not pc time.   
            writer.writerow({'Timestamp': timer,'PC_time': pcTimer, 'pcapData': finalEntry[j]})
            count += 1
            last = j

    # print("running pcapCsvToDs...")
    # import pcapCsvToDs
    # pcapCsvToDs.main(room_filename_csv=LABELED_ARUCO_FILE_PATH,display_graphs=False)

    print("finished\nrunning the pcap data fix script...")
    import pcapFix 
    pcapFix.main()

    print("running placement fix script...")
        
    df = pd.read_csv("dataset_fixed.csv")
    lablesArr = df.columns
    newList = []

    newList.append(lablesArr[0])    # pcap time
    newList.extend(lablesArr[6:])   # pcap data
    newList.append(lablesArr[1])    # pc time
    # newList.append(lablesArr[5])    # lable
    # newList.extend(lablesArr[2:5])  # x y z

    df = df[newList]

    df.to_csv(r'Results/dataset_room_'+ ROOM_NUMBER + '_baseline_pcap_' + PCAP_NUM + '.csv', index = False, header = True)
    print("finished!\n")