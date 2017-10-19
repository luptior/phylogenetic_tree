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

        # smooth the curve
        y_smooth = []
        for i in range(1, len(ydata) - 1):
            y_smooth.append((ydata[i - 1] + ydata[i] + ydata[i + 1]) / 3)


        # find the intersection of derivative and x axis with data points
        for i in range(len(der)):
            if der[i] * der[i + 1] < 0:
                thres = i + 2
                break
        print(f"threshold = {thres}")

        # find a cutoff value to fit num
        cut = der[thres]*2
        for x in range(thres, len(y_smooth)):
            if y_smooth[x] < cut:
                cutoff = x
                break
        print(cutoff)
        fit_num = cutoff
        plt.scatter(cutoff, y_smooth[cutoff], label="cutoff")

        # plot the derivative
        plt.plot(xdata[1:fit_num], ydata[2:fit_num + 1], label="histogram")
        plt.plot(xdata[1:fit_num], y_smooth[1:fit_num], label="smooth curve")
        plt.plot(xdata[1:fit_num], der[1:fit_num], label="derivative")

        # find the peaks and troughs on the derivative
        der_extrema = []
        for i in range(thres, fit_num-5):
            if der[i] <= der[i + 1] >= der[i + 2]:
                der_extrema.append(i)
            elif der[i] >= der[i + 1] <= der[i + 2]:
                der_extrema.append(i)
            else:
                continue
        der_extrema = np.add(der_extrema, 2)
        print(f"extrema = {der_extrema}")

        plt.scatter(thres, y_smooth[thres], label="threshold")
        plt.scatter(der_extrema, [der[i] for i in der_extrema], label="extrema")

        peak = []
        if len(der_extrema) % 2 == 1:
            for i in [2*x for x in range(int(3/2)+1)]:
                print(i)
                if i == 0:
                    peak.append(int((thres + der_extrema[0])/2))
                else:
                    peak.append(int((der_extrema[i - 1] + der_extrema[i]) / 2))
        else:
            for i in [2 * x for x in range(int(len(der_extrema) / 2))]:
                peak.append(int((der_extrema[i] + der_extrema[i + 1]) / 2))

        """     
        with open("%s" % (file[:-4] + "_thres.txt"), "w") as myfile:
            myfile.write("%d" % thres)
        """
        peak = np.add(peak, -1)
        plt.scatter(peak, [y_smooth[i] for i in peak], label="peaks")
        plt.legend()
        plt.savefig("%s" % (file[:-4] + ".png"))
        plt.clf()


if __name__ == "__main__":
    filelist = sys.argv[1:]

    main()
