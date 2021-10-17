from numpy.core.numeric import NaN
import numpy
import pandas as pd
import pandas
from datetime import datetime
import time
import matplotlib.pyplot as plt
from scipy.stats import linregress
import csv 
import sys


def get_xp_and_fp_for_interp(data_frame, colomn_name, return_time = False):
    """Gives you the xp and fp from the visble aruco position on one dimension (x,y or z) """
    data_frame_no_nan = data_frame[(data_frame[colomn_name] <= 0) | (data_frame[colomn_name] >= 0) & (data_frame[colomn_name] != '')]  #Removes NaN from the data_frame
    if(not return_time): 
        return data_frame_no_nan[colomn_name].tolist()
    else:
        return data_frame_no_nan["ms"].tolist(), data_frame_no_nan[colomn_name].tolist()

def time_array_to_float_array(time_array):
    """Turns an array of strtime into an array containing the milisec-value of the time"""
    time_array_float = []
    for element in time_array:
        time_temp,milisec = element.split(".") # 01:34, 457
        time_list = time_temp.split(':') # 1, 34

        time_array_float.append(int(time_list[0])*60*1000+int(time_list[1])*1000+int(milisec))
        
    return time_array_float

def replace_labels_with_ints(labels):
    """Returns a list of labels as intigers"""
    res = []
    for label in labels:
        if 'DO_NOT_USE' in label:
            res.append(0)
        elif 'laying down' in label:
            res.append(1)
        elif 'sitting' in label:
            res.append(2)
        elif 'walking' in label:
            res.append(3)
        elif 'standing' in label:
            res.append(4)
        else:
            res.append(-1)
    return res
    
def int_label_to_label(int_label):
  
    if int_label == 0:
        return "DO_NOT_USE"
    elif int_label == 1:
        return "laying down"
    elif int_label == 2:
        return "sitting"
    elif int_label == 3:
        return "walking"
    elif int_label == 4:
        return "standing"


def main(pcap_data_filename = "pcap_data.csv", room_filename_csv = None, pcap_data_output_filename = "pcapdata.csv", display_graphs = True):
    if room_filename_csv is None:
        room_filename_csv ="room_" + input("enter room num1: ") + ".csv"
    pcap_csv_data = pd.read_csv(pcap_data_filename)

    assert type(pcap_csv_data) != "None"

    pcap_csv_data.columns = ["Timestamp","PC_time", "finalEntry"]

    Timelist = list(pcap_csv_data.Timestamp) #pcap time
    PcTimelist = list(pcap_csv_data.PC_time)
    Datalist = list(pcap_csv_data.finalEntry)

    assert len(Timelist) == len(PcTimelist) and len(PcTimelist) == len(Datalist) and len(Datalist) != 0 

    room_file = pd.read_csv(room_filename_csv)

    assert type(room_file) != "None"
    room_file.columns = ["Time", "x", "y", "z", "ms", "Lable"]

    all_times_aruco = room_file["Time"].tolist() #aruco time

    assert all_times_aruco != None and len(all_times_aruco) != 0

    xp_time_float, fp_x = get_xp_and_fp_for_interp(room_file,'x',return_time=True) # takes out all the aruco person positions and time when we see person  
    fp_y = get_xp_and_fp_for_interp(room_file,'y')
    fp_z = get_xp_and_fp_for_interp(room_file,'z')

    all_times_aruco_float = time_array_to_float_array(all_times_aruco)
    assert len(xp_time_float) == len(fp_x) and len(fp_y) == len(fp_z) and len(xp_time_float) == len(fp_x) and len(fp_x) != 0
    assert NaN not in fp_x and NaN not in fp_y and NaN not in fp_z

    mslist = list(room_file.ms)
    lablelist = list(room_file.Lable)

    assert len(mslist) == len(lablelist) and len(mslist) != 0

    file_name = pcap_data_output_filename
    file = open(file_name,'w')

    assert file != None

    writer = csv.writer(file)

    assert writer != None
    writer.writerow(['pcapTime', 'PC_time','x','y','z','Lable','pcapData'])  #writing the first line to the csv file.

    listCount = []

    interpolated_data_x = numpy.interp(Timelist,xp_time_float,fp_x)
    interpolated_data_y = numpy.interp(Timelist,xp_time_float,fp_y)
    interpolated_data_z = numpy.interp(Timelist,xp_time_float,fp_z)
    assert len(interpolated_data_x) == len(interpolated_data_y) == len(interpolated_data_z) != 0 and len(Timelist) == len(interpolated_data_y)

    manual_labels_int = replace_labels_with_ints(lablelist)

    assert len(lablelist) == len(manual_labels_int)
    assert -1 not in manual_labels_int

    assert manual_labels_int[0] == 0

    labels_interp = numpy.interp(Timelist, mslist,manual_labels_int)

    if display_graphs:
        plt.plot(Timelist, labels_interp, '-',color='g')
        plt.plot(Timelist, interpolated_data_z, '-',color='r')
        plt.ticklabel_format(useOffset=False)
        plt.show()
    label_list = []
    for label_int in labels_interp:
        label_int = round(label_int)
        label_list.append(int_label_to_label(label_int))

    for i in range(len(Timelist)):
        assert writer.writerow([Timelist[i], PcTimelist[i], round(interpolated_data_x[i],2),round(interpolated_data_y[i],2), round(interpolated_data_z[i],2), label_list[i], Datalist[i]]) != None

if __name__ == '__main__':
    main()