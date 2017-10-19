import numpy as np
import sys
import matplotlib.pyplot as plt

fit_num = int(sys.argv[1])
fileslist = sys.argv[2:]

for f in fileslist:
    data = np.loadtxt(f)

    xdata = []
    ydata = []

    for dp in data:
        xdata.append(dp[0])
        ydata.append(dp[1])

    plt.plot(xdata[:fit_num], ydata[:fit_num])
    plt.ylim([0, 3*10**7])
    plt.title("Histogram of %s" % (f.split("/")[-1]))

    plt.savefig("%s.png"% (f[0:-4]))
    plt.clf()

