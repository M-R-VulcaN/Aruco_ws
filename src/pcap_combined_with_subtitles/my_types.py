
import parse
import pdb
import csv

def underscore_time_to_ms(time_str : str): 
    hours, minutes, seconds, millisec = parse.parse("{0}_{1}_{2}_{3}",time_str)
    return int(hours)*3600*1000+int(minutes)*60*1000+int(seconds)*1000+int(millisec)

class FrameLabeled:
    def __init__(self, label: str, frame_num: int):
        assert isinstance(label, str), 'You need to enter a str for label.'
        assert isinstance(frame_num, int), 'You need to enter a number for frame_num.'
        self.label = label
        self.frame_num = frame_num

    @staticmethod
    def loadListFromFile(labels_file):
        labels_reader = csv.reader(labels_file)
        fl_list = []
        for csv_line in labels_reader:
            fl_list.append(FrameLabeled(csv_line[1],int(csv_line[0])))
        return fl_list

class FrameTimestamped:
    def __init__(self,  timestamp_ms: float, frame_num: int):
        assert isinstance(timestamp_ms, int) or isinstance(timestamp_ms,float), 'You need to enter a number for timestamp_ms.'
        assert isinstance(frame_num, int), 'You need to enter a int for frame_num.'
        self.timestamp_ms = timestamp_ms 
        self.frame_num = frame_num


    @staticmethod
    def loadListFromFile(image_names_file):
        frame_ts_list = []
        image_names_file_lines = []
        for line in image_names_file:
            image_names_file_lines.append(line)
        assert len(image_names_file_lines) != 0, 'file is empty'
        image_names_file_lines.sort(key=lambda x: int(x.split('_')[0].replace('image', '')))
        # pdb.set_trace()
        for line in image_names_file_lines:
            parse_output = parse.parse("image{0}_{1}.jpg",line.replace('\n', ''))
            frame_number = int(parse_output[0])


            timestamp_str = parse_output[1]
            timestamp_ms = underscore_time_to_ms(timestamp_str)
            frame_ts_list.append(FrameTimestamped(timestamp_ms,frame_number))

        return frame_ts_list

class LabelTimestamped:
    def __init__(self,  timestamp_ms: float, label: str):
        assert isinstance(timestamp_ms, int) or isinstance(timestamp_ms,float), 'You need to enter a number for timestamp_ms.'
        assert isinstance(label, str), 'You need to enter a str for label.'
        self.timestamp_ms = timestamp_ms 
        self.label = label

    @staticmethod
    def mergeLabelsWithTimestamps(frames_ts_list:list , frames_labeled_list:list):
        assert isinstance(frames_ts_list, list), 'You need to enter a list for ft_list.'
        assert isinstance(frames_labeled_list, list), 'You need to enter a list for fl_list.'
        for ft in frames_ts_list:
            assert isinstance(ft, FrameTimestamped), 'You need to enter a list of only FrameTimestamped for ft_list.'
        for fl in frames_labeled_list:
            assert isinstance(fl, FrameLabeled), 'You need to enter a list of only FrameLabeled for fl_list.'

        assert len(frames_ts_list) != 0, 'frames_ts_list cannot be empty.'
        assert len(frames_labeled_list) != 0, 'frames_labeled_list cannot be empty.'

        lable_ts_list = []
        label_list_len = len(frames_labeled_list)
        assert label_list_len != 0, 'the label list is empty'
        curr_label_index = 0

        for ft in frames_ts_list:
            if ft.frame_num == frames_labeled_list[curr_label_index].frame_num:
                lable_ts_list.append(LabelTimestamped(ft.timestamp_ms,frames_labeled_list[curr_label_index].label))
                curr_label_index+= 1
                if curr_label_index == label_list_len:
                    break
        return lable_ts_list

    @staticmethod
    def save_list_to_csv(lt_list: list, path_to_file:str,end_ts:int):
        assert isinstance(lt_list, list), 'You need to enter a list for lt_list.'
        assert isinstance(path_to_file, str), 'You need to enter a str for path_to_file.'
        assert isinstance(end_ts, int), 'You need to enter a int for end_ts.'
        for lt in lt_list:
            assert isinstance(lt, LabelTimestamped), 'You need to enter a list of only LabelTimestamped for lt_list.'

        lt_list.sort(key=lambda x: x.timestamp_ms,reverse=False)
        assert len(lt_list) != 0,'lt_list cannot be empty'
        with open(path_to_file,'w') as out_csv_file:
            out_csv_file.write('Number;Start time in milliseconds;End time in milliseconds;"Text"\n')
            start_time = lt_list[0].timestamp_ms
            for i in range(0, len(lt_list)-1):
                out_csv_file.write(f'{i+1};{lt_list[i].timestamp_ms-start_time};{lt_list[i+1].timestamp_ms-start_time};"{lt_list[i].label}"\n')
            
            out_csv_file.write(f'{len(lt_list)};{lt_list[-1].timestamp_ms-start_time};{end_ts-start_time};"{lt_list[-1].label}"\n')
            

            
        




        

def main():
    #1
    fl= FrameLabeled(label="standing",frame_num=999)
    print(fl.__dict__)
    #2
    ft = FrameTimestamped(frame_num=999,timestamp_ms=9.0)
    print(ft.__dict__)
    #3  
    with open('images-temp.txt','w') as f:
        f.write('image00000_07_46_57_534.jpg\nimage0000318_07_22_50_029.jpg\nimage0000816_07_38_10_503.jpg\nimage00003038_07_37_47_041.jpg')
    labels_temp_file = open('labels-temp.txt','r')

    fl_list = FrameLabeled.loadListFromFile(labels_temp_file)
    for fl in fl_list:
        print(fl.__dict__)
    labels_temp_file.close()

    #4
    with open('labels-temp.txt','w') as f:
        f.write('0,DO_NOT_USE\n318,walking\n816,DO_NOT_USE\n862,walking\n1350,DO_NOT_USE')
    images_temp_file = open('images-temp.txt','r')

    ft_list = FrameTimestamped.loadListFromFile(images_temp_file)
    for ft in ft_list:
        print(ft.__dict__)
    images_temp_file.close()

    #5
    lt = LabelTimestamped(timestamp_ms=9.0,label='standing')
    print(lt.__dict__)

    #6
    print('l',len(fl_list))
    lt_list = LabelTimestamped.mergeLabelsWithTimestamps(ft_list, fl_list)
    for lt in lt_list:
        print(lt.__dict__)
    #7
    LabelTimestamped.save_list_to_csv(lt_list,'temp_lt.csv',ft_list[-1].timestamp_ms)

if __name__ == '__main__':
    main()