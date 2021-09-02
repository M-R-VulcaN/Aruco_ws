import pandas as pd
import pandas
"""
This code takes the dataset with the pcap data in it and adds in the lines that dont have the data with them.
"""
#pcap
data = pd.read_csv("test1.csv")
data.columns = ["pcapTime","Time","Aruco","x","y","z","Lable","ms","pcapData"]
pcapTime = list(data.pcapTime)
Time = list(data.Time)
Aruco = list(data.Aruco)
x = list(data.x)
y = list(data.y)
z = list(data.z)
Lable = list(data.Lable)
ms = list(data.ms)
pcapData = list(data.pcapData)

#data
room_10 = pd.read_csv("ds_room_10.csv")
room_10.columns = ["Time", "Aruco", "x", "y", "z", "ms", "Lable"]
tlist = list(room_10.Time)
mslist = list(room_10.ms)
idlist = list(room_10.Aruco)
xlist = list(room_10.x)
ylist = list(room_10.y)
zlist = list(room_10.z)
lablelist = list(room_10.Lable)

import csv 

print("pcapTime,Time,Aruco,x,y,z,Lable,ms,pcapData")
file_name = input("\nPlase enter the .csv file name: ")
file = open(file_name,'w')
writer = csv.writer(file)
writer.writerow(['pcapTime','Time','Aruco ID','x','y','z','Lable','ms','pcapData'])  #writing the first line to the csv file.


counter = 0
for i in range(len(ms)):
    alreadyEntered = False
    for j in range(len(mslist)):
        if(alreadyEntered == False):
            if (mslist[j] == ms[i]):
                alreadyEntered = True
                diff = j-counter
                for d in range(diff):
                    # print(d)
                    if(d == 0):
                        # print(counter + d)
                        writer.writerow([pcapTime[i-1], tlist[counter+d], idlist[counter+d], xlist[counter+d], ylist[j], zlist[counter+d], lablelist[counter+d], mslist[counter+d], pcapData[i-1]])
                        print(counter+d, pcapTime[i-1], tlist[counter+d], idlist[counter+d], xlist[counter+d], ylist[counter+d], zlist[counter+d], lablelist[counter+d], mslist[counter+d]) #pcapdatalist[i]
                    else:
                        writer.writerow(['', tlist[counter+d], idlist[counter+d], xlist[counter+d], ylist[counter+d], zlist[counter+d], lablelist[counter+d], mslist[counter+d]])
                        print(counter+d, " nan ", tlist[counter+d], idlist[counter+d], xlist[counter+d], ylist[counter+d], zlist[counter+d], lablelist[counter+d], mslist[counter+d], "   no match") #pcapdatalist[i]
                counter = j
            else:
                pass
        else:
            pass



