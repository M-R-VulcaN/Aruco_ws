import os 
import sys
import csv
import parse
from  datetime import datetime
from constants import *


def get_frames_labeled_list(labels_reader):
    """returns a list of tuples with length of 2 with the follow pattern: (FRAME_NUMBER, LABEL_NAME)"""
    res = []
    for line in labels_reader:
        frame_num = int(line[0])
        label_name = line[1]
        res.append((frame_num, label_name))
    return res

def timestamp_frames_labeled_list(frames_labeled, image_names_file ):
    res = []
    curr_frame_index = 0
    frames_labeled_len = len(frames_labeled)
    
    image_names_file_lines = []
    for line in image_names_file:
        image_names_file_lines.append(line)

    image_names_file_lines.sort(key=lambda x: int(x.split('_')[0].replace('image', '')))
  
    for line in image_names_file_lines:
        parse_output = parse.parse("image{0}_{1}.jpg\n",line)
        frame_number = int(parse_output[0])

        if frame_number != frames_labeled[curr_frame_index][0]:
            continue

        timestamp_str = parse_output[1]
        # timestamp_ms = datetime.strptime(timestamp_str, '%H_%M_%S_%f').timestamp() * 1000
        res.append((timestamp_str,frames_labeled[curr_frame_index][1]))
        curr_frame_index += 1
        if frames_labeled_len == curr_frame_index:
            break
    
    # for item in res:
        

    return res


def main():
    labels_file = open(LABELS_FILE_PATH,'r')
    image_names_file = open(IMAGE_NAMES_FILE_PATH,'r')
    dataset_0_file = open(DATASET_FILES_PATHS[0],'r')
    output_0_file = open(OUTPUT_FILES_PATHS[0],'w')
    
    labels_reader = csv.reader(labels_file)
    frames_labeled = get_frames_labeled_list(labels_reader)

    dataset_0_reader = csv.reader(dataset_0_file)
    output_0_writer = csv.reader(output_0_file)

    label_index = 0
    timestamps_labeled = timestamp_frames_labeled_list(frames_labeled, image_names_file)
    # for dataset_line in dataset_0_reader:
    print(timestamps_labeled)
    exit(0)
        



    labels_file.close()
    dataset_0_file.close()
    output_0_file.close()

if __name__ == '__main__':
    main()

