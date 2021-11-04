import pandas as pd
import yaml
import os

#the directory that contain the csv's
main_dir_path = "/home/makeruser/Desktop/record-wifi-results/room_"

def get_user_choise():
    room_number = input("enter room number: ")
    # room_number = 0
    all_csv = input("fix all 4 csv? y/n : ")
    if(all_csv == 'y'):
        pcap_number = [0,1,2,3]
    # pcap_number = [0,1,2,3]
    else:
        pcap_number = input("enter csv number: ")
    # pcap_number = 0
    return room_number,pcap_number

def replace_labels_mistakes(df,labelList):
    for i in range(len(labelList)-1):
        if(labelList[i] != labelList[i+1] and labelList[i] != labelList[i-1]):

            print(i-1, labelList[i-1])
            print(i, labelList[i])
            print(i+1, labelList[i+1])

            print("need to replace (", i, labelList[i] ,") with 'DO_NOT_USE'\n\n")
            df.loc[i, 'Lable'] = 'DO_NOT_USE'
            # import pdb
            # pdb.set_trace()

def replace_to_nan(df):
    df.loc[df['Lable'] == 'DO_NOT_USE', 'x'] = 'Nan'
    df.loc[df['Lable'] == 'DO_NOT_USE', 'y'] = 'Nan'
    df.loc[df['Lable'] == 'DO_NOT_USE', 'z'] = 'Nan'
    df.loc[df['Lable'] == 'DO_NOT_USE', 'Lable'] = 'Nan'

def read_room_size_from_yaml(room_number):
    with open(main_dir_path + str(room_number) +'/params.yaml', 'r') as stream:
        data_loaded = yaml.safe_load(stream)
        room = (data_loaded["locations"]["room"]["x"],
        data_loaded["locations"]["room"]["y"],
        data_loaded["locations"]["room"]["z"])
        print("room: ", room)
        # print(room[0])
        return room

def write_to_csv(df,room_number,pcap_number):
    # Absolute path of a file
    old_name = main_dir_path + str(room_number) + '/dataset_room_' + str(room_number) + '_pcap_' + str(pcap_number) +'.csv'
    new_name = main_dir_path + str(room_number) + '/dataset_room_' + str(room_number) + '_pcap_' + str(pcap_number) +'_old.csv'

    # Renaming the file
    os.rename(old_name, new_name)

    df.to_csv(main_dir_path + room_number + '/dataset_room_' + room_number + '_pcap_' + str(pcap_number) +'.csv', index = False, header = True)



def main():
    room_number,pcap_number = get_user_choise()

    for csv in pcap_number:
        print("\nfixing dataset for:\nroom: {}\ncsv: {}".format(room_number,csv))
        df = pd.read_csv(main_dir_path + str(room_number) + '/dataset_room_' + str(room_number) + '_pcap_' + str(csv) +'.csv')

        labelList = df['Lable'].tolist()
        xList = df['x'].tolist()
        yList = df['y'].tolist()
        zList = df['z'].tolist()

        replace_labels_mistakes(df,labelList)

        replace_to_nan(df)

        room = read_room_size_from_yaml(room_number)

        outCount = 0
        zCount = 0

        for index in range(len(zList)-1):
            if(zList[index] != 'Nan'):

                #replacing places that 'Z' is higher than 1.64m, usually at the end of each movement
                if(float(zList[index])>1.64):
                    print("Z is higher than 1.64 m: ", index, zList[index])
                    df.loc[df['z'] == zList[index], 'Lable'] = 'Nan'
                    df.loc[df['z'] == zList[index], 'x'] = 'Nan'
                    df.loc[df['z'] == zList[index], 'y'] = 'Nan'
                    df.loc[df['z'] == zList[index], 'z'] = 'Nan'
                    zCount+=1

                #check if the 'x' value is out of the room(getting room measures from the yaml file)
                if(float(xList[index]) > room[0]):
                    print("X is out of the room: ", index, xList[index])
                    outCount+=1

                #check if the 'y' value is out of the room(getting room measures from the yaml file)
                if(float(yList[index]) > room[1]):
                    print("Y is out of the room: ", index, yList[index])
                    outCount+=1
        print("\n\n===============================================")
        print("PLOT:\n{} times Z is higher than 1.64m\n{} times x or y out of the room\n\nrun the script again to see if there any mistakes left.".format(zCount, outCount))
        
        ## this will change the columns names but it will not match the names in the "plot_data.py"
        # print("renaming columns...")
        # df.rename(columns={'pcapTime': 'pcap_time',
        #                    'Lable': 'label',
        #                    'PC_time': 'pc_time'},inplace=True, errors='raise')
        # print("finished")

        write_to_csv(df,room_number,csv)



if __name__ == '__main__':
    main()