import os 
import sys
import csv

PCAP_FILES_AMOUNT = 4


#<paths>
ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
RES_DIR = f'{ROOT_DIR}/res'
OUTPUT_DIR = f'{ROOT_DIR}/output'

#<argv>
if len(sys.argv) == 1:
    print('usage: enter the room number')
    exit(1)


CURR_ROOM_NUM_INDEX = 1


try:
    CURR_ROOM_NUM = int(sys.argv[CURR_ROOM_NUM_INDEX])
except ValueError:
    print('Error: make sure that the room number is an integer')
    exit(2)
#</argv> 

ROOM_DIR = f'{RES_DIR}/room_{CURR_ROOM_NUM}'
LABELS_FILE_PATH = f'{ROOM_DIR}/room_{CURR_ROOM_NUM}_images.csv'
IMAGE_NAMES_FILE_PATH = f'{ROOM_DIR}/image_names.txt'
OUTPUT_FILES_PATHS = [f'{OUTPUT_DIR}/dataset_room_{CURR_ROOM_NUM}_pcap_{pcap_num}.csv' for pcap_num in range(PCAP_FILES_AMOUNT)]

DATASET_FILES_PATHS = [f'{ROOM_DIR}/dataset_room_{CURR_ROOM_NUM}_pcap_{pcap_num}.csv' for pcap_num in range(PCAP_FILES_AMOUNT)]
#</paths>



def get_frame_timestamps(image_names_list):


def main():
    labels_file = open(LABELS_FILE_PATH,'r')
    image_names_file = open(IMAGE_NAMES_FILE_PATH,'r')
    dataset_0_file = open(DATASET_FILES_PATHS[0],'r')
    output_0_file = open(OUTPUT_FILES_PATHS[0],'w')

    labels_reader = csv.reader(labels_file)
    dataset_0_reader = csv.reader(dataset_0_file)
    output_0_writer = csv.reader(output_0_file)

    label_index = 0
    dataset_index = 0

    while True:
        curr_row_dataset = next(dataset_0_reader)
        curr_row_label = next(dataset_0_reader)



    labels_file.close()
    dataset_0_file.close()
    output_0_file.close()

if __name__ == '__main__':
    main()

