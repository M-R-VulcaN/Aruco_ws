import pandas as pd
import pandas

"""
This code reads the pcap_data csv and write it to a new csv file with the ds_room csv
compares the ms from both files.
"""

data = pd.read_csv("pcap_data.csv")
data.columns = ["Timestamp", "PC_time", "pcapData"]
Timelist = list(data.Timestamp)
PcTimelist = list(data.PC_time)
Datalist = list(data.pcapData)

print(len(Timelist))
print(len(Datalist))


room_10 = pd.read_csv("data_room_10.csv")
room_10.columns = ["Time", "Aruco", "x", "y", "z", "ms", "Lable"]
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
print(PcTimelist[0])

count = -1
already = False
place = 0

import csv 
print("pcapTime,Time,x,y,z,Lable,ms,pcapData")
# file_name = input("\nPlase enter the .csv file name: ")
file_name = 'pcapdata.csv'
file = open(file_name,'w')
writer = csv.writer(file)
writer.writerow(['pcapTime','PC_time','x','y','z','Lable','ms','pcapData'])  #writing the first line to the csv file.

listCount = []

for i in range(len(Timelist)):
    alreadyEntered = False
    for j in range(len(mslist)):
        if(alreadyEntered == False):
            if (mslist[j] == Timelist[i]):
                # print(Timelist[i], "               ", mslist[j])
                print(j, Timelist[i], PcTimelist[i], tlist[j], xlist[j], ylist[j], zlist[j], lablelist[j], mslist[j]) #pcapdatalist[i]
                writer.writerow([Timelist[i], PcTimelist[i], xlist[j], ylist[j], zlist[j], lablelist[j], mslist[j], Datalist[i]])
                #            "pcapTime,Time,Aruco ID,x,y,z,Lable,ms,pcapData"
                alreadyEntered = True
                count += 1
                listCount.extend([j])           
            #         102         104
            elif (Timelist[i] < mslist[j]):
                #       104         102        102            101
                if(mslist[j] - Timelist[i] > Timelist[i] - mslist[j - 1]): #            
                    # print(Timelist[i], "            ", mslist[j - 1], "           ", Timelist[i] - mslist[j - 1], "                1")
                    print(j, Timelist[i], PcTimelist[i], tlist[j-1], xlist[j-1], ylist[j-1], zlist[j-1], lablelist[j-1], mslist[j-1]) #pcapdatalist[i]
                    writer.writerow([Timelist[i], PcTimelist[i], xlist[j-1], ylist[j-1], zlist[j-1], lablelist[j-1], mslist[j-1], Datalist[i]])
                else:
                    # print(Timelist[i], "            ", mslist[j], "           ", mslist[j] - Timelist[i],  "                2")
                    print(j, Timelist[i], PcTimelist[i], tlist[j], xlist[j], ylist[j], zlist[j], lablelist[j], mslist[j]) #pcapdatalist[i]
                    writer.writerow([Timelist[i], PcTimelist[i], xlist[j], ylist[j], zlist[j], lablelist[j], Timelist[i], Datalist[i]])
                alreadyEntered = True
                count += 1
                place = j
                listCount.extend([j]) 
            else:
                pass
        else:
            pass
    
    if (count != i):
        print(j)
        print(j-1)
        print(j, Timelist[i], PcTimelist[i], tlist[j-1], xlist[j-1], ylist[j-1], zlist[j-1], lablelist[j-1], mslist[j-1]) #pcapdatalist[i]
        writer.writerow([Timelist[i], PcTimelist[i], xlist[j-1], ylist[j-1], zlist[j-1], lablelist[j-1], Timelist[i], Datalist[i]])
        # print(j, Timelist[i], PcTimelist[i], '', '', '', '', '', 'DO_NOT_USE', Timelist[i]) #pcapdatalist[i]
        # writer.writerow([Timelist[i], PcTimelist[i], '', '', '', '', '', 'DO_NOT_USE', Timelist[i], Datalist[i]])
        
print(len(Timelist))


