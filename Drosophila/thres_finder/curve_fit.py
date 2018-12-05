from scipy.optimize import curve_fit
import sys
import numpy as np

fit_num = int(sys.argv[1])
fileslist = sys.argv[2:]

for f in fileslist:
    
    xdata = []
    ydata = []
    for dp in np.loadtxt(f):
        xdata.append(int(dp[0]))
        ydata.append(int(dp[1]))
    
    

