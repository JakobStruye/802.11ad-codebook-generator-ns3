import sys
import matplotlib.pyplot as plt
import numpy as np
from collections import deque


fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax1.set_yscale("log")
#colors = deque(["blue", "orange", "lightblue", "yellow"])
for argi in range(1,len(sys.argv)):
    xper = []
    xrxpow = []
    per = []
    rxpow = []
    with open(sys.argv[argi], "r") as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith("+"):
                splits = line.split(" ")
                if True:# int(splits[4].split("=")[1]) < 5000:
                    time = float(splits[0][1:-1])
                    if True:# time < 0.13:
                        if splits[1] == "PER":
                            xper.append(time)
                            per.append(float(splits[2]))#.split("=")[1][:-1]))
                        elif splits[1] == "RXPOW":
                            xrxpow.append(time)
                            rxpow.append(float(splits[2]))#.split("=")[1][:-1]))
                    else:
                        break


    #ax1.plot(xper,per, label="PER", color=colors.popleft())
    filename = sys.argv[argi].split("/")[-1]
    ax2.plot(xrxpow, rxpow, label=filename + " RX Power (db)")#, color=colors.popleft())
#for rot in np.arange(0,0.45,0.001):
#    ax1.axvline(rot, color="grey", alpha=0.5, lw=1)
plt.legend()
#ax2.set_ylim(top=-40,bottom=-42)
plt.show(block=True)