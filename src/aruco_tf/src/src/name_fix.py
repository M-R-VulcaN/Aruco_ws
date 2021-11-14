import pandas as pd
import yaml
import os

#the directory that contain the csv's
main_dir_path = "/home/makeruser/Desktop/dataset/data"

def get_user_choise():
    # room_number = input("enter room number: ")
    room_number = [0,1,2,3,4,11,12,13,14,100]
    # all_csv = input("fix all 4 csv? y/n : ")
    # if(all_csv == 'y'):
        # pcap_number = [0,1,2,3]
    pcap_number = [0,1,2,3]
    # else:
        # pcap_number = input("enter csv number: ")
    # pcap_number = 0
    return room_number,pcap_number

def write_to_csv(df,room_number,pcap_number):
    # Absolute path of a file
    old_name = main_dir_path + '/dataset_room_' + str(room_number) + '_pcap_' + str(pcap_number) +'.csv'
    new_name = main_dir_path + '/dataset_room_' + str(room_number) + '_pcap_' + str(pcap_number) +'_old.csv'

    # Renaming the file
    os.rename(old_name, new_name)

    df.to_csv(main_dir_path + '/dataset_room_' + str(room_number) + '_pcap_' + str(pcap_number) +'.csv', index = False, header = True)

def main():
    room_number,pcap_number = get_user_choise()
    for room_number in room_number:
        print (room_number)
        
        for csv in pcap_number:
            print("\nfixing dataset for:\nroom: {}\ncsv: {}".format(str(room_number),csv))
            df = pd.read_csv(main_dir_path + '/dataset_room_' + str(room_number) + '_pcap_' + str(csv) +'.csv')

            outCount = 0
            zCount = 0

            # this will change the columns names but it will not match the names in the "plot_data.py"
            print("renaming columns...")
            try:
                df.rename(columns={'pcapTime': 'pcap_time',
                                    'Lable': 'label',
                                    'PC_time': 'pc_time'},inplace=True, errors='raise')
            except Exception as e:
                print(e)
            print("finished")

            write_to_csv(df,room_number,csv)



if __name__ == '__main__':
    main()