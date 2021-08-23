import csv
from numpy.lib import index_tricks
import pandas as pd

# lable = input("enter lable: ")
# starting = '00:00:0.033'#input("enter starting time: ")
# ending = '00:05:9.870'#input("enter ending time: ")
# end = False

# with open('test.csv', 'r') as csvfile:
#     data = csv.DictReader(csvfile)
#     # writer = csv.writer(csvfile)
#     print("---------------------------------")
#     for row in data:

#         print(row['Time:'])

#         if(row['Time:'] == starting or row['Time:'] != ending and end == False):
#             with open('innovators.csv', 'a', newline='') as file:
#                 writer = csv.writer(file)
#                 writer.writerow([row['Time:'], lable, row['Aruco ID'], row['x'], row['y'], row['z']])
#         elif(row['Time:'] == ending):
#             with open('innovators.csv', 'a', newline='') as file:
#                 writer = csv.writer(file)
#                 writer.writerow([row['Time:'], lable, row['Aruco ID'], row['x'], row['y'], row['z']])
#                 end = True
#         else:
#             with open('innovators.csv', 'a', newline='') as file:
#                 writer = csv.writer(file)
#                 writer.writerow([row['Time:'], "none", row['Aruco ID'], row['x'], row['y'], row['z']])



# df = pd.read_csv("innovators.csv")
# df.head(3) #prints 3 heading rows
# # df.set_value(1, "Lables:", 30)
# df.loc[df["Time:"]=="00:00:0.033", "Lables"] = 5
# df.to_csv("innovators.csv", index=False)

import pandas as pd
df = pd.read_csv("test.csv")
# print(df) #prints 3 heading rows

# if(df.loc[["Time:"]=="00:00:0.033"]):
# print(df.loc[['Time:'] == "00:00:0.033"])
# print(df.loc[5:10])

print(df.loc[df['Time:'] == '00:00:0.033'])

df.loc[['00:00:0.033', '00:00:0.066'], ['Lable:']] = 2
print(df)


# df.loc[df["Time:"]=="00:00:0.033", "Lable:"] = 5
# df.to_csv("innovators.csv", index=False)