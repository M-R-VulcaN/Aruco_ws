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

DEFAULT_PATH = input("please enter PCAP file name: ")
# DEFAULT_PATH = "output.pcap"

if __name__ == "__main__":
    path: str=DEFAULT_PATH
    reader = get_reader(path)
    csi_data = reader.read_file(path)
    print ("csi_data.frames: ",len(csi_data.frames))
    finalEntry, no_frames, no_subcarriers = get_CSI(csi_data, metric=None, squeeze_output=True)
    print ("csi_data.timestamps: ",len(csi_data.timestamps))
    count = 0
    j = -1
    # file_name = input("please enter file name: ")
    file_name = 'pcap_data.csv'
    with open(file_name, 'w') as csvfile:
        fieldnames = ['Timestamp', 'PC_time','pcapData']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        print("writing to file...")
        writer.writeheader()
        for i in csi_data.timestamps:
            j += 1
            pcTimer = i
            # print(pcTimer)
            timer = (i - csi_data.timestamps[0])*1000
            #1627975155.109669-1627972936.190185       #in order to represent time in ms and not pc time.
            writer.writerow({'Timestamp': timer,'PC_time': pcTimer, 'pcapData': finalEntry[j]})
            count += 1
            last = j
            # writer.writerow({'PC_time': pcTimer})
        print("finished writing data to file.\n\n")
        print("\nfirst pcap data: \n", finalEntry[0])
        if (count != len(csi_data.frames)):
            print("\nempty data first stamp: \n",finalEntry[last+1])
            # writer.writerow({'pcapData': finalEntry[last]})
        # print("finished writing timestamps.\nwriting data...")
        # fd.write(myCsvRow)
        # for j ,frame in enumerate(finalEntry):
        #     writer.writerow({'pcapData': finalEntry[j]})
        # print("finished writing data.")

    # running the pcap fix script
    print("\nrunning the pcap data fix script...")
    import pcapFix