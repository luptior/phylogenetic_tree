import numpy as np


def read_histogram(file):
    # load data from histogram.txt file to var data
    # return smoothed y and derivative as list
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
    y_smooth.append(ydata[0])
    for i in range(1, len(ydata) - 1):
        y_smooth.append((ydata[i - 1] + ydata[i] + ydata[i + 1]) / 3)
    y_smooth.append(ydata[-1])

    return xdata, y_smooth, der


def find_thres(der):
    # find the intersection of derivative and x axis with data points
    # return thres and cutoff x
    for i in range(len(der)):
        if der[i] * der[i + 1] < 0:
            thres = i + 2
            break
    return thres


def find_fitnum(thres, der, y_smooth):
    # find a cutoff value to fit num
    cut = der[thres] * 2
    for x in range(thres, len(y_smooth)):
        if y_smooth[x] < cut:
            cutoff = x
            break
        else:
            cutoff = int(len(y_smooth)/10)
    return cutoff


def find_peaks(thres, fit_num, der):
    # find the peaks and troughs on the derivative
    der_extrema = []
    for i in range(thres, fit_num - 5):
        if der[i] <= der[i + 1] >= der[i + 2]:
            der_extrema.append(i)
        elif der[i] >= der[i + 1] <= der[i + 2]:
            der_extrema.append(i)
        else:
            continue
    der_extrema = np.add(der_extrema, 2)

    peak = []
    if len(der_extrema) % 2 == 1:
        for i in [2 * x for x in range(int(3 / 2) + 1)]:
            if i == 0:
                peak.append(int((thres + der_extrema[0]) / 2))
            else:
                peak.append(int((der_extrema[i - 1] + der_extrema[i]) / 2))
    else:
        for i in [2 * x for x in range(int(len(der_extrema) / 2))]:
            peak.append(int((der_extrema[i] + der_extrema[i + 1]) / 2))

    peak = np.add(peak, 1)
    return peak


