from scipy.optimize import curve_fit
import sys
import numpy as np
import thres_peaks as tp
import matplotlib.pyplot as plt

fileslist = sys.argv[1:]


def norm(x, mu, sigma, a):
    return a / (sigma * np.sqrt(2 * np.pi)) * np.exp(-np.power(x - mu, 2) / 2 / np.power(sigma, 2))


def error(x, a, b, c, d):
    return a / (b + c * np.power(x, d))


def func(x, a, b, c, d, e, f, g):
    return error(x, a, b, c, d) + norm(x, e, f, g)


def func2(x, a, b, c, d, e, f, g, e2, f2, g2):
    return error(x, a, b, c, d) + norm(x, e, f, g) + norm(x, e2, f2, g2)


def func3(x, a, b, c, d, e, f, g, e2, f2, g2, e3, f3, g3):
    return error(x, a, b, c, d) + norm(x, e, f, g) + norm(x, e2, f2, g2) + norm(x, e3, f3, g3)

for f in fileslist:
    xdata, ydata, der = tp.read_histogram(f)
    thres = tp.find_thres(der)
    fit_num = tp.find_fitnum(thres, der, ydata)
    peaks = tp.find_peaks(thres, fit_num, der)

    # print(f'peaks: {peaks}')
    # plt.plot(xdata[:fit_num], ydata[:fit_num], label="original")
    # plt.scatter(thres, ydata[thres], label='threshold')

    if len(peaks) == 0:
        sys.exit("no normal distribution curves to fit")
    elif len(peaks) == 1:
        popt, pcov = curve_fit(func, xdata[1:], ydata[1:],
                               p0=[10**8, 1, 1, 1, peaks[0], 5, 10**7], maxfev=10**5)

        for x in range(1, fit_num):
            print(x, norm(x, *popt[4:]) - error(x, *popt[:4]))
            if (norm(x, *popt[4:]) - error(x, *popt[:4])) * (norm(x+1, *popt[4:]) - error(x+1, *popt[:4])) < 0:
                thres2 = x
                if thres2 != 1 :
                    with open("%s"%(f[:-4]+"_thres.txt"), "w") as myfile:
                        myfile.write("%d" % thres)
                        break
        print(thres2)
        # plt.plot(xdata[1:fit_num], func(xdata[1:fit_num], *popt), label='fit')
        # plt.plot(xdata[1:fit_num], error(xdata[1:fit_num], *popt[:4]), label='error')
        # plt.plot(xdata[1:fit_num], norm(xdata[1:fit_num], *popt[4:]), label='norm')
    elif len(peaks) == 2:
        popt, pcov = curve_fit(func2, xdata[1:], ydata[1:],
                               p0=[10 ** 8, 1, 1, 1, peaks[0], 5, 10 ** 7, peaks[1], 5, 10 ** 7], maxfev=10**6)

        thres2 = []
        for x in range(1, fit_num):
            if (norm(x, *popt[4:7]) - error(x, *popt[:4])) * (norm(x+1, *popt[4:7]) - error(x+1, *popt[:4])) < 0:
                if x != 1:
                    thres2.append(x)
                    break
        for x in range(1, fit_num):
            if (norm(x, *popt[7:]) - error(x, *popt[:4])) * (norm(x+1, *popt[7:]) - error(x+1, *popt[:4])) < 0:
                if x != 1:
                    thres2.append(x)
                    break
        print(thres2)
        with open("%s"%(f[:-4]+"_thres.txt"), "w") as myfile:
            myfile.write("%d" % min(thres2))
        # plt.plot(xdata[1:fit_num], func2(xdata[1:fit_num], *popt), label='fit')
        # plt.plot(xdata[1:fit_num], error(xdata[1:fit_num], *popt[:4]), label='error')
        # plt.plot(xdata[1:fit_num], norm(xdata[1:fit_num], *popt[4:7]), label='norm1')
        # plt.plot(xdata[1:fit_num], norm(xdata[1:fit_num], *popt[7:]), label='norm2')
    elif len(peaks) == 3:
        popt, pcov = curve_fit(func3, xdata[1:], ydata[1:],
                               p0=[10 ** 8, 1, 1, 1, peaks[0], 5, 10 ** 7, peaks[1], 5, 10 ** 7, peaks[2], 5, 10 ** 7], maxfev=10**6)

        thres2 = []
        for x in range(1, fit_num):
            if (norm(x, *popt[4:7]) - error(x, *popt[:4])) * (norm(x + 1, *popt[4:7]) - error(x + 1, *popt[:4])) < 0:
                if x != 1:
                    thres2.append(x)
                    break
        for x in range(1, fit_num):
            if (norm(x, *popt[7:10]) - error(x, *popt[:4])) * (norm(x + 1, *popt[7:10]) - error(x + 1, *popt[:4])) < 0:
                if x != 1:
                    thres2.append(x)
                    break
        for x in range(1, fit_num):
            if (norm(x, *popt[10:]) - error(x, *popt[:4])) * (norm(x + 1, *popt[10:]) - error(x + 1, *popt[:4])) < 0:
                if x != 1:
                    thres2.append(x)
                    break
        with open("%s" % (f[:-4] + "_thres.txt"), "w") as myfile:
            myfile.write("%d" % min(thres2))
        print(thres2)
        # plt.plot(xdata[1:fit_num], func3(xdata[1:fit_num], *popt), label='fit')
        # plt.plot(xdata[1:fit_num], error(xdata[1:fit_num], *popt[:4]), label='error')
        # plt.plot(xdata[1:fit_num], norm(xdata[1:fit_num], *popt[4:7]), label='norm1')
        # plt.plot(xdata[1:fit_num], norm(xdata[1:fit_num], *popt[7:10]), label='norm2')
        # plt.plot(xdata[1:fit_num], norm(xdata[1:fit_num], *popt[10:]), label='norm2')
    else:
        print(peaks)
        sys.exit("too many normal distribution curves to fit")

