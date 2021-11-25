import os 
import sys
import csv

PCAP_FILES_AMOUNT = 4


#<paths>
ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
RES_DIR = f'{ROOT_DIR}/res'

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
SUBTITLE_FILE_PATH = f'{ROOM_DIR}/room_{CURR_ROOM_NUM}_images.csv'
IMAGE_NAMES_FILE_PATH = f'{ROOM_DIR}/image_names.txt'
PCAP_FILES_PATHS = [f'{ROOM_DIR}/dataset_room_{CURR_ROOM_NUM}_pcap_{pcap_num}.csv' for pcap_num in range(PCAP_FILES_AMOUNT)]
#</paths>

def main():
    subtitles_file = open(SUBTITLE_FILE_PATH,'r')
    pcap_0_file = open(PCAP_FILES_PATHS[0],'r')

if __name__ == '__main__':
    main()

