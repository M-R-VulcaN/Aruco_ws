import os 
import sys
import csv
import parse
from  datetime import datetime
import constants as cons
import my_types as tp

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
    labels_file = open(cons.LABELS_FILE_PATH,'r')
    image_names_file = open(cons.IMAGE_NAMES_FILE_PATH,'r')
    print()
    dataset_0_file = open(cons.DATASET_FILES_PATHS[0],'r')
    output_0_file = open(cons.OUTPUT_FILES_PATHS[0],'w')
    
    labeled_frames = tp.FrameLabeled.loadListFromFile(labels_file)
    timestamped_frames = tp.FrameTimestamped.loadListFromFile(image_names_file)
    timestamped_labels = tp.LabelTimestamped.mergeLabelsWithTimestamps(timestamped_frames, labeled_frames)
    tp.LabelTimestamped.save_list_to_csv(timestamped_labels, f'{cons.OUTPUT_DIR}/room_{cons.CURR_ROOM_NUM}_subtitles.csv', timestamped_frames[-1].timestamp_ms)
    labels_file.close()
    dataset_0_file.close()
    output_0_file.close()

if __name__ == '__main__':
    main()

