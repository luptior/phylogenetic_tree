import numpy as np
import sys
import matplotlib.pyplot as plt


def main(fit_num, filelist):
    for file in filelist:

        # load data from histogram.txt file to var data
        data = np.loadtxt(file)

        xdata = []
        ydata = []
        der = []

        for dp in data[:]:
            xdata.append(dp[0])
            ydata.append(dp[1])

        # store the derivative
        for i in range(len(ydata)-1):
            der[i] = ydata[i+1]-ydata[i]

        # plot the derivative
        plt.plot(xdata[1:], der, label="Derivative")

        # find the intersection of derivative and x axis
        roots = []
        for i in range(len(der)-1):
            if der[i] * der[i+1] < 0:
                roots.append(i)



        thres = 0

        for i in range(200):
            if sum(ydata[i:i+3]) <= sum(ydata[i+1:i+4]) >= sum(ydata[i+2:i+5]):
                thres = i + 2
                break
        with open("%s"%(file[:-4]+"_thres.txt"), "w") as myfile:
            myfile.write("%d"%thres)




if __name__ == "__main__":
    fit_num = int(sys.argv[1])
    f_list = sys.argv[2:]

    main(fit_num, f_list)
