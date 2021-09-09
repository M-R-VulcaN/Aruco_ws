from numpy.core.numeric import NaN
import numpy
import pandas as pd
import pandas
from datetime import datetime
import time
import matplotlib.pyplot as plt
from scipy.stats import linregress

STANDING_HEIGHT_MIN_M = 1.3 
LAYING_DOWN_HEIGHT_M = 0.5
LAYING_DOWN_HEIGHT_M = 0.5
MOVEMENT_SLOPE = 0.00004
"""
This code reads the pcapdata csv and write it to a new csv file with the ds_room csv
compares the ms from both files.
"""

def get_xp_and_fp_for_interp(data_frame, colomn_name, return_time = False):
    """Gives you the xp and fp from the visble aruco position on one dimension (x,y or z) """
    data_frame_no_nan = data_frame[(data_frame[colomn_name] <= 0) | (data_frame[colomn_name] >= 0)]  #Removes NaN from the data_frame
    if(not return_time): 
        return data_frame_no_nan[colomn_name].tolist()
    else:
        return data_frame_no_nan["Time"].tolist(), data_frame_no_nan[colomn_name].tolist()

def time_array_to_float_array(time_array):
    """Turns an array of strtime into an array containing the milisec-value of the time"""
    time_array_float = []
    for element in time_array:
        time_temp,milisec = element.split(".") # 00:01:34, 457
        time_list = time_temp.split(':') # 0, 1, 34

        # 0*3600*1000 + 1*60*1000+ 34*1000 + 457 = 94457 [milisec]       
        time_array_float.append(int(time_list[0])*3600*1000+int(time_list[1])*60*1000+int(time_list[2])*1000+int(milisec))
        
    return time_array_float

def is_standing_or_walking(z_axis):
    return z_axis >= STANDING_HEIGHT_MIN_M

def is_sitting(z_axis):
    return z_axis < STANDING_HEIGHT_MIN_M and z_axis > LAYING_DOWN_HEIGHT_M

def is_laying_down(z_axis):
    return z_axis <= LAYING_DOWN_HEIGHT_M

def autolabeling(time_list,x_list,y_list,z_list):
    """returns label list"""
    label_list = []
    
    for i in range(0,len(time_list),10):
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
            if is_sitting(average_z):
                label_list.append('sitting')
            elif is_laying_down(average_z):
                label_list.append('laying_down')
            elif is_standing_or_walking(average_z):

                biggest_slope = max([x_lgress.slope, y_lgress.slope, z_lgress.slope])
                # print('biggest_slope', biggest_slope)
                if biggest_slope > MOVEMENT_SLOPE:
                    label_list.append('walking')
                else:
                    label_list.append('standing')
        
    return label_list

            

    
    

pcap_csv_data = pd.read_csv("pcapdata.csv")
pcap_csv_data.columns = ["Timestamp", "finalEntry"]
pcap_timestamps = list(pcap_csv_data.Timestamp)
Datalist = list(pcap_csv_data.finalEntry)

print(len(pcap_timestamps))
print(len(Datalist))


room_10 = pd.read_csv("data_room_10.csv")
# room_10.columns = ["Time", "Aruco", "x", "y", "z", "ms", "Lable"]
room_10.columns = ["Time", "Lable", "Aruco", "x", "y", "z", "ms"]

all_times_aruco =  room_10["Time"].tolist()

xp_time, fp_x = get_xp_and_fp_for_interp(room_10,'x',return_time=True)
fp_y = get_xp_and_fp_for_interp(room_10,'y')
fp_z = get_xp_and_fp_for_interp(room_10,'z')
xp_time_float = time_array_to_float_array(xp_time)
all_times_aruco_float = time_array_to_float_array(all_times_aruco)


# print(xp_time[0],type(fp_x[0]),type(fp_y[0]),type(all_times_aruco[0]))
print('fp_xf',fp_x)
# input('pause fp')
interpolated_data = numpy.interp(xp_time_float,xp_time_float,fp_x)
print("interpolated:")
for i in range(len(interpolated_data)):
    print(all_times_aruco[i], interpolated_data[i])


# input('pause')
tlist = list(room_10.Time)
mslist = list(room_10.ms)
idlist = list(room_10.Aruco)
xlist = list(room_10.x)
ylist = list(room_10.y)
zlist = list(room_10.z)
lablelist = list(room_10.Lable)

print(len(mslist))
print(mslist[0])
print(pcap_timestamps[0])


count = -1
already = False
place = 0

import csv 
print("pcapTime,Time,Aruco,x,y,z,Lable,ms,pcapData")
file_name = input("\nPlase enter the .csv file name: ")
file = open(file_name,'w')
writer = csv.writer(file)
writer.writerow(['pcapTime', 'Aruco','x','y','z','Lable','ms','pcapData'])  #writing the first line to the csv file.

listCount = []
print('tp',pcap_timestamps[i])
# timelist_float = time_array_to_float_array(Timelist)
interpolated_data_x = numpy.interp(pcap_timestamps,xp_time_float,fp_x)
interpolated_data_y = numpy.interp(pcap_timestamps,xp_time_float,fp_y)
interpolated_data_z = numpy.interp(pcap_timestamps,xp_time_float,fp_z)

# t_full=np.linspace(0, 9, 10)
# t_no_nans = [0,1,2,3,6,7,8,9]
# y = [0,1,2,3,6,7,8,9]

# yinterp = np.interp(t_full, t_no_nans, y)
# plt.plot(xp_time_float, fp_x, 'o',color='c')
# plt.plot(xp_time_float, fp_y, 'o',color='m')
# plt.plot(xp_time_float, fp_z, 'o',color='tab:pink')
# plt.plot(Timelist, interpolated_data_x, '-x',color='g')

#plot in XY plane
plt.plot(interpolated_data_y, interpolated_data_x, '-x',color='g')
plt.plot(fp_y, fp_x, 'o',color='r')
print(autolabeling(pcap_timestamps, interpolated_data_x, interpolated_data_y, interpolated_data_z))
input('pause')
#plot in XZ plane
# plt.plot(interpolated_data_x, interpolated_data_z, '-x',color='g')
# plt.plot(fp_x, fp_z, 'o',color='r')

# plt.plot(Timelist, interpolated_data_y, '-x',color='y')
# plt.plot(Timelist, interpolated_data_z, '-x',color='r')
# plt.plot(t_full, yinterp, '-x')
plt.ticklabel_format(useOffset=False)
plt.show()

# input('pause plot')
for i in range(len(pcap_timestamps)):
    writer.writerow([pcap_timestamps[i], round(interpolated_data_x[i], 2), round(interpolated_data_y[i], 2), round(interpolated_data_z[i], 2),lablelist[i],mslist[i],Datalist[i]])


print(len(pcap_timestamps))


