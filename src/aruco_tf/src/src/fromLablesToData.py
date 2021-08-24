import intervaltree

data = intervaltree.IntervalTree()
res_file = open("res.csv", "w")
tofill = open("tofill.csv", "r").read()
data_container = open("data.csv", "r").read()

for line in data_container.split('\n')[1:]:
    line_values = line.split(';')
    data[int(line_values[1]) : int(line_values[2])] = line_values[3]

for line in tofill.split('\n')[1:-1]:
    timeval = float(line.split(',')[-1])
    node = data[timeval]

    if node:
        tree_node = list(node)[0]
        resline = line + ', ' + str(tree_node.data)
        res_file.write(resline + '\n')

res_file.close()
