import intervaltree
import sys

START_TIME_INDEX = 1
END_TIME_INDEX = 2
LABEL_INDEX = 3

CSV_LABELS_FILENAME = ""
OUTPUT_FILE_FILENAME = ""
ARUCO_POSITION_FILENAME = ""

CSV_LABELS_FILE_PATH_INDEX = 1
ARUCO_POSITIONS_FILE_PATH_INDEX = 2
OUTPUT_FILE_PATH_INDEX = 3

if len(sys.argv) < 4:
    room_number = input("enter room number: ")
    CSV_LABELS_FILENAME = "room_" + str(room_number) + "_labels.csv"
    OUTPUT_FILE_FILENAME = "room_" + str(room_number) + ".csv"
    ARUCO_POSITION_FILENAME = "room_" + str(room_number) + "_aruco.csv"
else:
    CSV_LABELS_FILENAME = sys.argv[CSV_LABELS_FILE_PATH_INDEX]
    OUTPUT_FILE_FILENAME = sys.argv[OUTPUT_FILE_PATH_INDEX]
    ARUCO_POSITION_FILENAME = sys.argv[ARUCO_POSITIONS_FILE_PATH_INDEX]

def get_label_intervaltree(csv_labels_filename = CSV_LABELS_FILENAME): 
    f = open(csv_labels_filename, "r")
    data_container = f.read()    # labelings
    for line in data_container.split('\n')[1:]:
        print(line)
    f.close()
    data = intervaltree.IntervalTree()

    for line in data_container.split('\n')[1:-1]:
        print('line', line)
        line_values = line.split(';')
        print(float(line_values[START_TIME_INDEX]))
        print(float(line_values[END_TIME_INDEX]))
        print(line_values[LABEL_INDEX])

        print()
        data[float(line_values[START_TIME_INDEX]) : float(line_values[END_TIME_INDEX])] = line_values[LABEL_INDEX].replace("\"","")
        print(line_values[LABEL_INDEX].replace("\"",""))
    return data


def main():
    
    res_file = open(OUTPUT_FILE_FILENAME, "w")
    tofill = open(ARUCO_POSITION_FILENAME, "r").read()       # aruco output
    data = get_label_intervaltree(CSV_LABELS_FILENAME)

    for line in tofill.split('\n')[1:-1]:
        timeval = float(line.split(',')[-1])
        node = data[timeval]

        if node:
            tree_node = list(node)[0]
            resline = line + ', ' + str(tree_node.data)
            res_file.write(resline + '\n')

    res_file.close()

if __name__ == '__main__':
    main()