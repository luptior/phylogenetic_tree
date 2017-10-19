import sys
import numpy as np


# return the 2 names of the species in the file name
# mode 1 return name in form specie1:specie2, mode 2 return name1 and name2 separately
def name_parse(name, mode):
    # index for the second dash
    if mode == 2:
        return name.split("_")[1], name.split("_")[2]
    elif mode == 1:
        return "%s:%s" % (name.split("_")[1], name.split("_")[2])
    else:
        sys.exit("wrong mode")


# take input of distance table and a row list with name inside corresponds to the row and column
def treegraph(dist_table, row, outfile):
    while len(row) > 1:
        # x, y for the index of the minimum dist
        x = 0
        y = 1
        min_dist = dist_table[0, 1]

        for i in range(0, len(row) - 1):
            for j in range(i + 1, len(row)):
                if i == j:
                    continue
                elif min_dist > dist_table[i, j]:
                    min_dist = dist_table[i, j]
                    x = i
                    y = j

        for j in range(0, len(row)):
            dist_table[x, j] = (dist_table[x, j] + dist_table[y, j]) / 2

        dist_table = np.delete(dist_table, y, 1)
        dist_table = np.delete(dist_table, y, 0)

        # merge the value of column at the same time

        row[x] = "(%s:%s, %s:%s)" % (row[x], min_dist, row[y], min_dist)
        del row[y]

    # while loop ends at column only has 1 element
    output = open(outfile, "w")
    output.write(row[0] + ";")
    output.close()


# take a file and sum distance inside
def sumdist(filename, mode):
    file = open(filename, "r")
    line = file.readline().split()
    print(line)
    if mode == "-unique":
        # mode read the unique kmer
        return line[0]
    elif mode == "-counts":
        # mode read the kmer conuts
        return line[1]


def main():
    mode = sys.argv[1]
    mode2 = sys.argv[2]
    outfile = sys.argv[3]
    filenames = sys.argv[4:]
    # take in input files names in a list

    name_list = []
    for name in filenames:
        name1, name2 = name_parse(name, 2)
        if name1 not in name_list:
            name_list.append(name1)
        if name2 not in name_list:
            name_list.append(name2)
    # get a list with all species names in it

    inter_list = {}
    for name in filenames:
        try:
            inter_list[name_parse(name, 1)] = sumdist(name, mode2)
        except:
            sys.exit("file wrong", name)
    # get a dict of specie1:specie2 as key, distance as value

    row = name_list

    l = len(name_list)
    dist_table = np.zeros((l, l))

    # construct table based on number of species number
    for i in range(l):
        for j in range(i + 1, l):
            if name_list[i] + ":" + name_list[j] in inter_list.keys():
                dist_table[i, j] = inter_list[name_list[i] + ":" + name_list[j]]
            else:
                dist_table[i, j] = inter_list[name_list[j] + ":" + name_list[i]]

    for i in range(1, l):
        for j in range(i):
            dist_table[i, j] = dist_table[j, i]

    if mode == "-n":
        treegraph(dist_table, row, outfile)
    elif mode == "-d":

        output = open(outfile, "w")
        data = str(len(name_list)) + "\n"
        for i in range(len(name_list)):
            row_data = ""
            for j in range(len(name_list)):
                row_data += str(dist_table[i][j]) + " "
            data += "%s %s\n" % (name_list[i], row_data)

        output.write(data)
        output.close()

    else:
        print("Options:\n n : print newick \n d : print distance table and store output file in *.dist")


if __name__ == "__main__":
    main()
