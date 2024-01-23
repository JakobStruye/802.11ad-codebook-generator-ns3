from generate import get_offset, Antenna
import math
import numpy as np
import sys

azimuthsCount = 361
elevationsCount = 181

sectorCount = int(sys.argv[2])

a = Antenna(id=1, orientation=(0,0), shape=(8,8), phaseBits=2, sectorCount=sectorCount, duplicateElements=False)

def azrange():
   return np.linspace(0, azimuthsCount - 1,  (azimuthsCount - 1) + 1) - 180
def elrange():
   # return np.linspace(-32, -22,11 )
   return np.linspace(0, elevationsCount - 1, (elevationsCount - 1) + 1) - 90

def mirrorWrap(angle):
    return angle + (np.sign(angle) * 90 - angle)*2

azs = []
els = []
steervecs = []
for az in azrange():
    testidx = 0
    for el in elrange():
        vals = []
        for e in a.elements:
            phase = -1 * math.pi * get_offset(element=e, azimuth=az, elevation=el)
            vals.append(np.exp(1j*phase))

        azs.append(az)
        els.append(el)
        vals = np.array(vals)
        steervecs.append(vals)

with open (sys.argv[1], "r") as f:

    lines = f.readlines()
    lines = lines[len(lines) - ((sectorCount+1)*4+1):]
    del(lines[4])
    print(lines[0:5])
    for i in range(sectorCount+1):
        l = lines[i*4+3]
        l = l.split(",")
        vals = []
        for j in range(len(l)//2):
            amp = float(l[j*2])
            ang = float(l[j*2+1])
            vals.append(amp * np.exp(1j * ang))
        arr = np.array(vals)
        best = 0
        bestidx = -1
        for steeridx in range(len(steervecs)):
            this_sv = steervecs[steeridx]
            result = np.matmul(np.atleast_2d(arr), np.atleast_2d(this_sv).T)
            if abs(result) > abs(best):
                best = result
                bestidx = steeridx
        possible_azs = (azs[bestidx], mirrorWrap(azs[bestidx]))
        print("Sector {} towards az {} or {}, el {} with gain {}".format(i if i > 0 else "QUASI", min(possible_azs), max(possible_azs), els[bestidx], abs(best)[0][0]))
