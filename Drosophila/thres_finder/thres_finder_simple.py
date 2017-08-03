import numpy as np
import sys


def main(filelist):
    for file in filelist:
        data = np.loadtxt(file)

        x = []
        y = []

        for dp in data[:]:
            x.append(dp[0])
            y.append(dp[1])

        thres = 0

        for i in range(200):
            if sum(y[i:i+3]) <= sum(y[i+1:i+4]) >= sum(y[i+2:i+5]):
                # use the average of 3 to avoid the fluctuation
                thres = i + 2
                break
        with open("%s"%(file[:-4]+"_thres.txt"), "w") as myfile:
            myfile.write("%d"%thres)

if __name__ == "__main__":
    files = sys.argv[1:]
    main(files)
