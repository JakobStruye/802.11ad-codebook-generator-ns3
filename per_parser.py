import sys
import matplotlib.pyplot as plt
import numpy as np
from collections import deque


fig, ax1 = plt.subplots()
#ax2 = ax1.twinx()
#ax2.set_yscale("log")
#colors = deque(["blue", "orange", "lightblue", "yellow"])
plotlines = []
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


    #ax2.plot(xper,per, label="PER", color=colors.popleft())
    filename = sys.argv[argi].split("/")[-1]
    plotline, = ax1.plot(xrxpow, rxpow, label=filename + " RX Power (db)")#, color=colors.popleft())
    plotlines.append(plotline)
#for rot in np.arange(0,0.45,0.001):
#    ax1.axvline(rot, color="grey", alpha=0.5, lw=1)
leg = plt.legend()
#ax1.set_ylim(top=-40,bottom=-42)


lined = dict()
for legline, origline in zip(leg.get_lines(), plotlines):
    legline.set_picker(True)  # 5 pts tolerance
    legline.set_pickradius(5)
    lined[legline] = origline


def onpick(event):
    legline = event.artist
    origline = lined[legline]
    vis = not origline.get_visible()
    origline.set_visible(vis)
    if vis:
        legline.set_alpha(1.0)
    else:
        legline.set_alpha(0.2)
    fig.canvas.draw()


fig.canvas.mpl_connect('pick_event', onpick)

plt.show(block=True)