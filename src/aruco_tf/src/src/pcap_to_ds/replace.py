import pandas as pd
import numpy as np

     
df = pd.read_csv("dataset_fixed.csv")
print(df.columns)

lablesArr = df.columns

print(len(lablesArr))

newList = []

newList.append(lablesArr[0])
newList.extend(lablesArr[7:])
newList.append(lablesArr[5])
newList.extend(lablesArr[2:5])
newList.append(lablesArr[1])
newList.append(lablesArr[6])

df = df[newList]

print(df)
room = input("enter room number: ")
df.to_csv(r'Results/dataset_room_'+ room + '.csv', index = False, header = True)
