from numpy.core.numeric import NaN
import numpy
import pandas as pd
import pandas
from datetime import datetime
import time
import matplotlib.pyplot as plt
from scipy.stats import linregress
import csv 
#import fromLablesToData
import sys

sys.path.append('/usr/local/bin/scripts_raw_data_to_dataset')

STANDING_HEIGHT_MIN_M = 0.8
LAYING_DOWN_HEIGHT_M = 0.5
LAYING_DOWN_HEIGHT_M = 0.25
MOVEMENT_SLOPE = 0.00004
DO_NOT_USE_TIME_GAP_MILLIS = 10000




"""
This code reads the pcapdata csv and write it to a new csv file with the ds_room csv
compares the ms from both files.
"""

debug_slope_list = ([],[])

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

        # 1*60*1000+ 34*1000 + 457 = 94457 [milisec]       
        time_array_float.append(int(time_list[0])*60*1000+int(time_list[1])*1000+int(milisec))
        
    return time_array_float

def debug_print(lst):
    print(len(lst), lst[:10])

def is_standing_or_walking(z_axis):
    return z_axis >= STANDING_HEIGHT_MIN_M

def is_sitting(z_axis):
    return z_axis < STANDING_HEIGHT_MIN_M and z_axis > LAYING_DOWN_HEIGHT_M

def is_laying_down(z_axis):
    return z_axis <= LAYING_DOWN_HEIGHT_M

def replace_labels_with_ints(labels):
    """Returns a list of labels as intigers"""
    res = []
    print('labels', len(labels), labels[:10])
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

def get_do_not_use_labels(time_list, original_time_aruco):
    res = []
    i = 0
    j = 0
    # print(tim)
    while len(time_list) < i and len(original_time_aruco) < j:
        if original_time_aruco[j]-DO_NOT_USE_TIME_GAP_MILLIS<= time_list[i] <= original_time_aruco[j]+DO_NOT_USE_TIME_GAP_MILLIS:
            res.append(None)
        elif original_time_aruco[j]-DO_NOT_USE_TIME_GAP_MILLIS > time_list[i]:
            res.append('DO_NOT_USE')
        if original_time_aruco[j]+DO_NOT_USE_TIME_GAP_MILLIS < time_list[i]:
            j+=1
        else:
            i+=1
    print('time_list:')
    debug_print(time_list)
    print('original_time_aruco:')
    debug_print(original_time_aruco)
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

def autolabeling(time_list,x_list,y_list,z_list,original_time_aruco):
    """returns label list"""
    label_list = get_do_not_use_labels(time_list, original_time_aruco)


    for i in range(0,len(label_list),10):
        partition= min(10,len(time_list)-i)
        # print('par:',partition)
        # print(time_list, x_list)
        # print('pass',time_list[i:partition],x_list[i:i+partition])
        x_lgress = linregress(time_list[i:i+partition],x_list[i:i+partition])
        y_lgress = linregress(time_list[i:i+partition],y_list[i:i+partition])
        z_lgress = linregress(time_list[i:i+partition],z_list[i:i+partition])
        # print('xyz slope:',x_lgress,y_lgress,z_lgress)

        average_z = numpy.mean(z_list[i:i+partition])
        
        for j in range(partition):
            if label_list[i+j] != None:
                continue
            if is_sitting(average_z):
                label_list[i+j] = 'sitting'
            elif is_laying_down(average_z):
                label_list[i+j] = 'laying down'
            elif is_standing_or_walking(average_z):
                
                # biggest_slope = max([x_lgress.slope, y_lgress.slope])
                amplitude_of_movement_vector = (x_lgress.slope**2 + y_lgress.slope**2)**0.5
                debug_slope_list[0].append(time_list[i+j])
                debug_slope_list[1].append(amplitude_of_movement_vector*10000)
                # print('biggest_slope', biggest_slope)
                if amplitude_of_movement_vector > MOVEMENT_SLOPE:
                    label_list[i+j] = 'walking'
                else:
                    label_list[i+j] = 'standing'
            else:
                label_list[i+j] = 'DO_NOT_USE'

        
    return label_list

            

    
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


    room_10 = pd.read_csv(room_filename_csv)

    assert type(room_10) != "None"
    room_10.columns = ["Time", "x", "y", "z", "ms", "Lable"]
    # room_10.columns = ["Time", "Aruco", "x", "y", "z", "ms",]

    all_times_aruco = room_10["Time"].tolist() #aruco time

    assert all_times_aruco != None and len(all_times_aruco) != 0

    xp_time_float, fp_x = get_xp_and_fp_for_interp(room_10,'x',return_time=True) # takes out all the aruco person positions and time when we see person  
    fp_y = get_xp_and_fp_for_interp(room_10,'y')
    fp_z = get_xp_and_fp_for_interp(room_10,'z')
    # xp_time_float = time_array_to_float_array(xp_time)
    all_times_aruco_float = time_array_to_float_array(all_times_aruco)
    assert len(xp_time_float) == len(fp_x) and len(fp_y) == len(fp_z) and len(xp_time_float) == len(fp_x) and len(fp_x) != 0
    assert NaN not in fp_x and NaN not in fp_y and NaN not in fp_z
    # print(xp_time[0],type(fp_x[0]),type(fp_y[0]),type(all_times_aruco[0]))
    print('fp_xf',fp_x)
    # input('pause fp')
    # interpolated_data = numpy.interp(xp_time_float,xp_time_float,fp_x)

    # assert len(interpolated_data) == len(xp_time_float)
    # print("interpolated:")
    # for i in range(len(interpolated_data)):
    #     print(all_times_aruco[i], interpolated_data[i])


    mslist = list(room_10.ms)

    lablelist = list(room_10.Lable)

    assert len(mslist) == len(lablelist) and len(mslist) != 0


    
    print("pcapTime,Time,Aruco,x,y,z,Lable,ms,pcapData")
    # file_name = input("\nPlase enter the .csv file name: ")
    file_name = pcap_data_output_filename
    file = open(file_name,'w')

    assert file != None

    writer = csv.writer(file)

    assert writer != None
    writer.writerow(['pcapTime', 'PC_time','x','y','z','Lable','pcapData'])  #writing the first line to the csv file.
    # writer.writerow(['pcapTime', 'PC_time','Aruco','x','y','z','Lable','ms','pcapData'])  #writing the first line to the csv file.

    listCount = []
    # print('tp',Timelist[i])
    # timelist_float = time_array_to_float_array(Timelist)

    print(len(fp_x), len(fp_y), len(fp_z))
    # input('pasue')
    interpolated_data_x = numpy.interp(Timelist,xp_time_float,fp_x)
    interpolated_data_y = numpy.interp(Timelist,xp_time_float,fp_y)
    interpolated_data_z = numpy.interp(Timelist,xp_time_float,fp_z)
    assert len(interpolated_data_x) == len(interpolated_data_y) == len(interpolated_data_z) != 0 and len(Timelist) == len(interpolated_data_y)
    print("timestamp len", len(Timelist))
    # t_full=np.linspace(0, 9, 10)
    # t_no_nans = [0,1,2,3,6,7,8,9]
    # y = [0,1,2,3,6,7,8,9]

    # yinterp = np.interp(t_full, t_no_nans, y)
    # plt.plot(xp_time_float, fp_x, 'o',color='c')
    # plt.plot(xp_time_float, fp_y, 'o',color='m')
    # plt.plot(xp_time_float, fp_z, 'o',color='tab:pink')
    # plt.plot(Timelist, interpolated_data_x, '-x',color='g')

    #plot in XY plane
    # plt.plot(interpolated_data_y, interpolated_data_x, '-x',color='g')
    # plt.plot(fp_y, fp_x, 'o',color='r')

    manual_labels_int = replace_labels_with_ints(lablelist)

    assert len(lablelist) == len(manual_labels_int)
    assert -1 not in manual_labels_int

    assert manual_labels_int[0] == 0
    # print(len(manual_labels_int), manual_labels_int[:10])
    # print(len(xp_time_float), xp_time_float[:10])


    labels_interp = numpy.interp(Timelist, mslist,manual_labels_int)
    # auotlabel_result = replace_labels_with_ints(autolabeling(Timelist, interpolated_data_x, interpolated_data_y, interpolated_data_z,xp_time_float))

    # debug_print(auotlabel_result)
    # debug_print(lablelist)
    # debug_print(manual_labels_int)
    # debug_print(labels_interp)

    # debug_print(Timelist)
    # input('pause')

    #plot autolabeling

    # comp = []
    # for i in range(len(Timelist)):
    #     if auotlabel_result[i] ==labels_interp[i]:
    #         comp.append(-2)
    #     else:
    #         comp.append(-1)

    # plt.plot(Timelist, auotlabel_result, '-',color='y')
    if display_graphs:
        plt.plot(Timelist, labels_interp, '-',color='g')
        # plt.plot(Timelist, comp, '-',color='r')
        # plt.plot(debug_slope_list[0], debug_slope_list[1], '-',color='r')
        # plt.plot()
        # plot in XZ plane
        # plt.plot(interpolated_data_x, interpolated_data_z, '-x',color='g')
        # plt.plot(fp_x, fp_z, 'o',color='r')

        # plt.plot(Timelist, interpolated_data_y, '-x',color='y')
        plt.plot(Timelist, interpolated_data_z, '-',color='r')
        # plt.plot(t_full, yinterp, '-x')
        plt.ticklabel_format(useOffset=False)
        plt.show()
    label_list = []
    for label_int in labels_interp:
        label_int = round(label_int)
        label_list.append(int_label_to_label(label_int))
    # input('pause plot')
    for i in range(len(Timelist)):
        assert writer.writerow([Timelist[i], PcTimelist[i], round(interpolated_data_x[i],2),round(interpolated_data_y[i],2), round(interpolated_data_z[i],2), label_list[i], Datalist[i]]) != None


    print(len(Timelist))


if __name__ == '__main__':
    main()