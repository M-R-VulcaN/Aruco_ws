import pandas as pd
import yaml
import os

#the directory that contain the csv's
main_dir_path = "/home/makeruser/Desktop/record-wifi-results/room_"

room_number = input("enter room number: ")
# room_number = 0
pcap_number = input("enter pcap number: ")
# pcap_number = 0

df = pd.read_csv(main_dir_path + str(room_number) + '/dataset_room_' + str(room_number) + '_pcap_' + str(pcap_number) +'.csv')

labelList = df['Lable'].tolist()
xList = df['x'].tolist()
yList = df['y'].tolist()
zList = df['z'].tolist()

# df.x.mul(0.88).to_csv(main_dir_path + str(room_number) + '/dataset_room_' + str(room_number) + '_pcap_' + str(pcap_number) +'.csv')
# df.y.mul(0.88).to_csv(main_dir_path + str(room_number) + '/dataset_room_' + str(room_number) + '_pcap_' + str(pcap_number) +'.csv')
# df.z.mul(0.88).to_csv(main_dir_path + str(room_number) + '/dataset_room_' + str(room_number) + '_pcap_' + str(pcap_number) +'.csv')

for i in range(len(labelList)-1):
    if(labelList[i] != labelList[i+1] and labelList[i] != labelList[i-1]):

        print(i-1, labelList[i-1])
        print(i, labelList[i])
        print(i+1, labelList[i+1])

        print("need to replace (", i, labelList[i] ,") with 'DO_NOT_USE'\n\n")
        df.loc[i, 'Lable'] = 'DO_NOT_USE'
        # import pdb
        # pdb.set_trace()

df.loc[df['Lable'] == 'DO_NOT_USE', 'x'] = 'Nan'
df.loc[df['Lable'] == 'DO_NOT_USE', 'y'] = 'Nan'
df.loc[df['Lable'] == 'DO_NOT_USE', 'z'] = 'Nan'
df.loc[df['Lable'] == 'DO_NOT_USE', 'Lable'] = 'Nan'

with open(main_dir_path + str(room_number) +'/params.yaml', 'r') as stream:
        data_loaded = yaml.safe_load(stream)
        room = (data_loaded["locations"]["room"]["x"],
        data_loaded["locations"]["room"]["y"],
        data_loaded["locations"]["room"]["z"])
        print("room: ", room)
        print(room[0])

outCount = 0
zCount = 0

for index in range(len(zList)-1):
    if(zList[index] != 'Nan'):
        # if(float(zList[index + 1]) - float(zList[index])>0.3):
        #     print(labelList[index], abs(float(zList[index + 1]) - float(zList[index])))
        #     df.loc[df['z'] == zList[index + 1], 'z'] = zList[index]
        #     import pdb
        #     pdb.set_trace()
        # if(float(zList[index]) - float(zList[index - 1])>0.3):
        #     print(labelList[index], abs(float(zList[index + 1]) - float(zList[index])))
        #     import pdb
        #     pdb.set_trace()


        # df.loc[df['z'] == zList[index], 'x'] = float(xList[index]).multiply(0.88)
        # df.loc[df['z'] == zList[index], 'y'] = float(yList[index]).multiply(0.88)
        # print(float(xList[index]))
        # print(float(yList[index]))
        # print(df.loc[df['z'] == zList[index], 'x'])
        # print(df.loc[df['z'] == zList[index], 'y'])
        # import pdb
        # pdb.set_trace()

        if(float(xList[index+1])-float(xList[index]) > 0.2):
            # print(df.loc[index, 'x'])
            df.loc[index+1, 'x'] = df.loc[index, 'x']
            print(float(xList[index+1])-float(xList[index]), float(xList[index+1]),float(xList[index]))
            import pdb
            pdb.set_trace()

        if(float(yList[index+1])-float(yList[index]) > 0.2):
            print(df.loc[index, 'x'])
            print(df.loc[index+1, 'x'])
            df.loc[index+1, 'y'] = df.loc[index, 'y']
            print(df.loc[index, 'x'])
            print(df.loc[index+1, 'x'])
            print("\n\n")
            print(float(yList[index+1])-float(yList[index]), float(yList[index+1]),float(yList[index]))
            import pdb
            pdb.set_trace()

        if(float(zList[index])>1.64):
            print("Z is higher than 1.64 m: ", index, zList[index])
            df.loc[df['z'] == zList[index], 'Lable'] = 'Nan'
            df.loc[df['z'] == zList[index], 'x'] = 'Nan'
            df.loc[df['z'] == zList[index], 'y'] = 'Nan'
            df.loc[df['z'] == zList[index], 'z'] = 'Nan'
            zCount+=1
        if(float(xList[index]) > room[0]):
            print("X is out of the room: ", index, xList[index])
            outCount+=1
        if(float(yList[index]) > room[1]):
            print("Y is out of the room: ", index, yList[index])
            outCount+=1

print("\n\nPLOT:\n{} times Z is higher than 1.64m\n{} times x or y out of the room".format(zCount, outCount))
## this will change the columns names but it will not match the names in the "plot_data.py"
# print("renaming columns...")
# df.rename(columns={'pcapTime': 'pcap_time',
#                    'Lable': 'label',
#                    'PC_time': 'pc_time'},inplace=True, errors='raise')
# print("finished")
# for index in range(len(zList)-1):
#     if(zList[index] != 'Nan'):
#         if(float(zList[index+1]) > float(zList[index]) + 0.15):
#             print(float(zList[index-2]), float(zList[index-1]), "{",float(zList[index]), float(zList[index+1]), "}", float(zList[index+2]))
#             df.loc[df['z'] == zList[index + 1], 'z'] = zList[index]
#         if(float(zList[index-1]) > float(zList[index]) + 0.15):
#             print(float(zList[index-2]), "{", float(zList[index-1]), float(zList[index]), "}", float(zList[index+1]), float(zList[index+2]))
#             df.loc[df['z'] == zList[index - 1], 'z'] = zList[index]


# Absolute path of a file
old_name = main_dir_path + str(room_number) + '/dataset_room_' + str(room_number) + '_pcap_' + str(pcap_number) +'.csv'
new_name = main_dir_path + str(room_number) + '/dataset_room_' + str(room_number) + '_pcap_' + str(pcap_number) +'_old.csv'

# Renaming the file
os.rename(old_name, new_name)

df.to_csv(r'/home/makeruser/Desktop/record-wifi-results/room_' + room_number + '/dataset_room_' + room_number + '_pcap_' + str(pcap_number) +'.csv', index = False, header = True)