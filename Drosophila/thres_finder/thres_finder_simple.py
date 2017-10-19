import numpy as np
import sys
import matplotlib.pyplot as plt

interlist = {
301:"Subobscura",
302:"Simulans",
303:"Yakuba",
304:"Teissieri",
305:"Miranda",
306:"Erecta",
307:"Orena",
308:"yakuba",
309:"Persimilis",
310:"Pseudoobscura",
311:"Mauritiana",
312:"Mauritiana2",
313:"Melanogaster",
314:"sechellia",
315: "Simulans",
316: "yakuba",
317: "yakuba"
}

def main(filelist):
    for file in filelist:
        data = np.loadtxt(file)

        xdata = []
        ydata = []

        for dp in data[:]:
            xdata.append(dp[0])
            ydata.append(dp[1])



        thres = 0

        for i in range(200):
            if sum(ydata[i:i+3]) <= sum(ydata[i+1:i+4]) >= sum(ydata[i+2:i+5]):
                # use the average of 3 to avoid the fluctuation
                thres = i + 2
                break
        # with open("%s"%(file[:-4]+"_thres.txt"), "w") as myfile:
        #    myfile.write("%d"%thres)

        fit_num = 200

        plt.title("%s" % ((file[28:31])+interlist[int(file[28:31])]+" downsampled"))
        plt.plot(xdata[:fit_num], ydata[:fit_num], label="original")
        plt.xlim([0, fit_num])
        plt.ylim([0, 2*10**7])
        plt.savefig("Fasta3/%s.png" % (file[28:31]))
        plt.clf()

if __name__ == "__main__":
    files = sys.argv[1:]
    main(files)
