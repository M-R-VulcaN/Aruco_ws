import intervaltree

START_TIME_INDEX = 1
END_TIME_INDEX = 2
LABEL_INDEX = 3
room_number = input("enter room number: ")
CSV_LABELS_FILENAME = "room_" + str(room_number) + "_labels.csv"

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
        print(int(line_values[START_TIME_INDEX]))
        print(int(line_values[END_TIME_INDEX]))
        print(line_values[LABEL_INDEX])

        print()
        data[int(line_values[START_TIME_INDEX]) : int(line_values[END_TIME_INDEX])] = line_values[LABEL_INDEX].replace("\"","")
        print(line_values[LABEL_INDEX].replace("\"",""))
    return data


def main():
    
    res_file = open("room_" + str(room_number) + ".csv", "w")
    tofill = open("room_" + str(room_number) + "_aruco.csv", "r").read()       # aruco output
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