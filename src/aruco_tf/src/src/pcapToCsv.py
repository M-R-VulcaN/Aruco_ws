"""
This code loads the pcap file and write its Timestamp and Data to the csv file
"""

import matplotlib.pyplot as plt
import numpy as np
import csv

from CSIKit.util.csitools import get_CSI
from CSIKit.util.filters import bandpass, hampel, running_mean
from CSIKit.reader import get_reader

DEFAULT_PATH = "output.pcap"

if __name__ == "__main__":
    path: str=DEFAULT_PATH
    reader = get_reader(path)
    csi_data = reader.read_file(path)
    print ("csi_data.frames: ",len(csi_data.frames))
    finalEntry, no_frames, no_subcarriers = get_CSI(csi_data, metric=None, squeeze_output=True)
    print ("csi_data.timestamps: ",len(csi_data.timestamps))
    # print(len(finalEntry[0]))
    # total_length = finalEntry.size
    # print(total_length)

    # print (csi_data.timestamps)
    # print (finalEntry)
    # print (finalEntry[5])


    with open('pcapdata.csv', 'w') as csvfile:
        fieldnames = ['Timestamp', 'finalEntry']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for i in csi_data.timestamps:
            timer = (i - csi_data.timestamps[0])*1000
            #1627975155.109669-1627972936.190185                #!!!
            writer.writerow({'Timestamp': timer})

        for j ,frame in enumerate(finalEntry):
            writer.writerow({'finalEntry': finalEntry[j]})
        print("finished")
