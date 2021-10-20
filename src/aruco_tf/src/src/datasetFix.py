import pandas as pd


main_dir_path = "/home/makeruser/Desktop/record-wifi-results/room_"

room_number = input("enter room number: ")
# room_number = 0

df = pd.read_csv(main_dir_path + str(room_number) + '/dataset_room_' + str(room_number) + '_pcap_0.csv')

labelList = df['Lable'].tolist()
xList = df['x'].tolist()
yList = df['y'].tolist()
zList = df['z'].tolist()

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

import yaml
with open(main_dir_path + str(room_number) +'/params.yaml', 'r') as stream:
        data_loaded = yaml.safe_load(stream)
        room = (data_loaded["locations"]["room"]["x"],
        data_loaded["locations"]["room"]["y"],
        data_loaded["locations"]["room"]["z"])
        print("room: ", room)
        print(room[0])

for z in range(len(zList)-1):
    if(zList[z] != 'Nan'):
        if(float(zList[z])>1.8):
            print(z, zList[z])
            df.loc[df['z'] == zList[z], 'x'] = 'Nan'
            df.loc[df['z'] == zList[z], 'y'] = 'Nan'
            df.loc[df['z'] == zList[z], 'z'] = 'Nan'
            df.loc[df['z'] == zList[z], 'Lable'] = 'Nan'
    # if(df['Lable'] == 'sitting' and float(zList[z]) > 1.5):
    #     print(float(zList[z]))
        if(float(xList[z]) > room[0] or float(yList[z]) > room[1]):
            print(xList[z])
            print(yList[z])
            # import pdb
            # pdb.set_trace()


## this will change the columns names but it will not match the names in the "plot_data.py"
# print("renaming columns...")
# df.rename(columns={'pcapTime': 'pcap_time',
#                    'Lable': 'label',
#                    'PC_time': 'pc_time'},inplace=True, errors='raise')
# print("finished")

df.to_csv(r'/home/makeruser/Desktop/record-wifi-results/room_' + room_number + '/dataset_room_' + room_number + '.csv', index = False, header = True)