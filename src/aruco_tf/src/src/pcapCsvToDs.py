from numpy.core.numeric import NaN
import numpy
import pandas as pd
import pandas
from datetime import datetime
import time
import matplotlib.pyplot as plt
from scipy.stats import linregress

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
        return data_frame_no_nan["Time"].tolist(), data_frame_no_nan[colomn_name].tolist()

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
        if label == 'DO_NOT_USE':
            res.append(0)
        elif label == 'laying down':
            res.append(1)
        elif label == 'sitting':
            res.append(2)
        elif label == 'walking':
            res.append(3)
        elif label == 'standing':
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

            

    
    

pcap_csv_data = pd.read_csv("pcapdata.csv")
pcap_csv_data.columns = ["Timestamp", "finalEntry"]
Timelist = list(pcap_csv_data.Timestamp)
Datalist = list(pcap_csv_data.finalEntry)

print(len(Timelist))
print(len(Datalist))


room_10 = pd.read_csv("data_room_10.csv")
room_10.columns = ["Time", "Aruco", "x", "y", "z", "ms", "Lable"]
# room_10.columns = ["Time", "Aruco", "x", "y", "z", "ms",]

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
print(Timelist[0])


count = -1
already = False
place = 0

import csv 
print("pcapTime,Time,Aruco,x,y,z,Lable,ms,pcapData")
# file_name = input("\nPlase enter the .csv file name: ")
file_name = 'temp.csv'
file = open(file_name,'w')
writer = csv.writer(file)
writer.writerow(['pcapTime','Time','Aruco','x','y','z','Lable','ms','pcapData'])  #writing the first line to the csv file.

listCount = []
print('tp',Timelist[i])
# timelist_float = time_array_to_float_array(Timelist)

print(len(fp_x), len(fp_y), len(fp_z))
# input('pasue')
interpolated_data_x = numpy.interp(Timelist,xp_time_float,fp_x)
interpolated_data_y = numpy.interp(Timelist,xp_time_float,fp_y)
interpolated_data_z = numpy.interp(Timelist,xp_time_float,fp_z)

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
# print(len(manual_labels_int), manual_labels_int[:10])
# print(len(xp_time_float), xp_time_float[:10])


labels_interp = numpy.interp(Timelist, mslist,manual_labels_int)
auotlabel_result = replace_labels_with_ints(autolabeling(Timelist, interpolated_data_x, interpolated_data_y, interpolated_data_z,xp_time_float))

debug_print(auotlabel_result)
debug_print(lablelist)
debug_print(manual_labels_int)
debug_print(labels_interp)

debug_print(Timelist)
input('pause')

#plot autolabeling

comp = []
for i in range(len(Timelist)):
    if auotlabel_result[i] ==labels_interp[i]:
        comp.append(-2)
    else:
        comp.append(-1)

plt.plot(Timelist, auotlabel_result, '-',color='y')
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

# input('pause plot')
for i in range(len(Timelist)):
    writer.writerow([Timelist[i],interpolated_data_x[i], interpolated_data_y[i], interpolated_data_z[i],lablelist[i],mslist[i],Datalist[i]])

# input('pause')
# for i in range(len(Timelist)):
#     alreadyEntered = False
#     for j in range(len(mslist)):
#         if(alreadyEntered == False):
#             if (mslist[j] == Timelist[i]):
#                 # print(Timelist[i], "               ", mslist[j])
#                 print(j, Timelist[i], tlist[j], idlist[j], xlist[j], ylist[j], zlist[j], lablelist[j], mslist[j]) #pcapdatalist[i]
#                 writer.writerow([Timelist[i], tlist[j], idlist[j], xlist[j], ylist[j], zlist[j], lablelist[j], mslist[j], Datalist[i]])
#                 #            "pcapTime,Time,Aruco ID,x,y,z,Lable,ms,pcapData"
#                 alreadyEntered = True
#                 count += 1
#                 listCount.extend([j])           
#             #         102         104
#             elif (Timelist[i] < mslist[j]):
#                 #       104         102        102            101
#                 if(mslist[j] - Timelist[i] > Timelist[i] - mslist[j - 1]): #            
#                     # print(Timelist[i], "            ", mslist[j - 1], "           ", Timelist[i] - mslist[j - 1], "                1")
#                     print(j, Timelist[i], tlist[j-1], idlist[j-1], xlist[j-1], ylist[j-1], zlist[j-1], lablelist[j-1], mslist[j-1]) #pcapdatalist[i]
#                     writer.writerow([Timelist[i], tlist[j-1], idlist[j-1], xlist[j-1], ylist[j-1], zlist[j-1], lablelist[j-1], mslist[j-1], Datalist[i]])
#                 else:
#                     # print(Timelist[i], "            ", mslist[j], "           ", mslist[j] - Timelist[i],  "                2")
#                     print(j, Timelist[i], tlist[j], idlist[j], xlist[j], ylist[j], zlist[j], lablelist[j], mslist[j]) #pcapdatalist[i]
#                     writer.writerow([Timelist[i], tlist[j], idlist[j], xlist[j], ylist[j], zlist[j], lablelist[j], mslist[j], Datalist[i]])
#                 alreadyEntered = True
#                 count += 1
#                 place = j
#                 listCount.extend([j]) 
#             else:
#                 pass
#         else:
#             pass
    
#     if (count != i):
#         print(j, Timelist[i], tlist[j], idlist[j], xlist[j], ylist[j], zlist[j], lablelist[j], mslist[j]) #pcapdatalist[i]
#         writer.writerow([Timelist[i], Timelist[i], idlist[j], xlist[j], ylist[j], zlist[j], lablelist[j], Timelist[i], Datalist[i]])

print(len(Timelist))


