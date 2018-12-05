import numpy as np
import sys
import matplotlib.pyplot as plt


def main():
    for file in filelist:

        # load data from histogram.txt file to var data
        data = np.loadtxt(file)

        xdata = []
        ydata = []
        der = []

        for dp in data:
            xdata.append(dp[0])
            ydata.append(dp[1])

        # store the derivative
        for i in range(len(ydata) - 1):
            der.append(ydata[i + 1] - ydata[i])

        # plot the derivative
        plt.plot(xdata[1:fit_num], ydata[1:fit_num], label="histogram")
        plt.plot(xdata[1:fit_num], der[1:fit_num], label="Derivative")

        # find the intersection of derivative and x axis with data points
        roots = []
        for i in range(fit_num):
            if der[i] * der[i + 1] < 0:
                roots.append(i)
        roots = np.add(roots, 2)
        print(roots)
        plt.scatter(roots, [der[i] for i in roots])

        thres = 0

        for i in range(200):
            if sum(ydata[i:i + 3]) <= sum(ydata[i + 1:i + 4]) >= sum(ydata[i + 2:i + 5]):
                thres = i + 2
                break
                
        with open("%s" % (file[:-4] + "_thres.txt"), "w") as myfile:
            myfile.write("%d" % thres)

        plt.show()


if __name__ == "__main__":
    fit_num = int(sys.argv[1])
    filelist = sys.argv[2:]

    main()
