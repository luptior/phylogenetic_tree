import matplotlib.pyplot as plt
import numpy as np
import sys

def main(files):
    for file in files:
        data = np.loadtxt(file)

        dist_table = np.zeros((int(data[0]), int(data[0])))
        name_list = []

        i = 0
        for row in data:
            name_list.append(row[0])
            dist_table[i][:]=row[1:]
            i+=1


if __name__ == "__main__":
    files = sys.argv[1:]
    main(files)
