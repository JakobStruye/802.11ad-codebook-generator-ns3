from math import sin, cos, pi, prod
import numpy as np
import sys
filename = "codebookParam"
antennaCount = 1
azimuthsCount = 361
elevationsCount = 181
cardinality_multiplier = 1
cardinality_multiplier_elev = 1

antennaSize = (8,8)

class Complex:
    def __init__(self, *, amplitude, phase):
        self.amplitude = amplitude
        self.phase = phase

    def quantize(self, *, amplitudeBits, phaseBits):
        pass

class Antenna:
    def __init__(self, *, id, orientation=(0,0), shape, phaseBits, amplitudeBits=1, sectorCount, duplicateElements=False):
        self.id = id
        self.orientation = orientation
        self.elementCount = prod(shape)
        if duplicateElements:
            self.elementCount *= 2
        self.phaseBits = phaseBits
        self.amplitudeBits = amplitudeBits
        self.directivity = None
        self.sectorCount = sectorCount
        self.sectors=[]

        self.elements = []
        if not type(shape) == tuple:
            shape = (shape, 1)
        for _ in range(2 if duplicateElements else 1):
            for x in range(shape[0]):
                for y in range(shape[1]-1, -1, -1):
                    elpos = (x - ((shape[0] - 1) / 2), y - ((shape[1]-1) / 2))
                    # 0.25 SPACING
                    elpos = (elpos[0]/2, elpos[1]/2)
                    # print(elpos)
                    self.elements.append(Element(*elpos))
    def add_sector(self, sector):
        self.sectors.append(sector)

class Element:
    def __init__(self, x_index, y_index ):
        self.x_index = x_index
        self.y_index = y_index

class Sector:
    def __init__(self, *, id, type=2, usage=2, azimuth, elevation):
        self.id = id
        self.type = type
        self.usage = usage
        self.azimuth = azimuth
        self.elevation = elevation

    def get_phase_for_element(self, element):
        return pi * get_offset(element, self.azimuth, self.elevation)


def get_offset(element, azimuth, elevation):
    return ( - element.x_index * sin(rad(azimuth)) * cos(rad(elevation)) + element.y_index * sin(rad(elevation)))

def rad(degree):
    return degree / 180. * pi

def azrange():
   return np.linspace(0, azimuthsCount - 1, cardinality_multiplier * (azimuthsCount - 1) + 1) - 180
def elrange():
   return np.linspace(0, elevationsCount - 1, cardinality_multiplier_elev * (elevationsCount - 1) + 1) - 90

def write_to_file(antennas):
    with open(filename, "w") as f:
        f.write("1\n") #number of rf chains
        f.write(str(len(antennas)) + '\n')
        for a in antennas:
            f.write(str(a.id) + "\n")
            f.write("1\n") #rf id
            f.write(str(a.orientation[0]) + "\n")
            f.write(str(a.orientation[1]) + "\n")
            f.write(str(a.elementCount) + "\n")
            f.write(str(a.phaseBits) + "\n")
            f.write(str(a.amplitudeBits) + "\n")
            # Directivity (i.e. gain)
            directivityString = ",".join((cardinality_multiplier_elev * (elevationsCount - 1) + 1) * ["1.000000"]) + "\n"
            for _ in azrange():
                f.write(directivityString)
            for e_idx, e in enumerate(a.elements):
                print(e_idx)
                for az in azrange():
                    vals = []
                    testidx = 0
                    for el in elrange():
                        testidx += 1
                        vals.append("1.000000")
                        phase = -1 * pi * get_offset(element=e, azimuth=az, elevation=el)
                        vals.append("{:.6f}".format(phase))
                        if vals[-1] == "-0.000000":
                            vals[-1] = "0.000000"
                    f.write(",".join(vals) + "\n")

            #QuasiOmni AWV
            # f.write("1.000000,0.000000," + (",".join((a.elementCount-1)*["1.000000,0.000000"])) + "\n")

            #CUSTOM QUASI
            with open ("phases_small_v2.txt", "r") as phasefile:
                phases = phasefile.readlines()
                phases = [float(l) for l in phases]


            # phases = prod(antennaSize) * ["0.000000"]
            phases = [str(ph) for ph in phases]
            f.write("1.000000," + ",1.000000,".join(phases) + "\n")

            ##OTHER QUASI
            # vals = []
            # for element in a.elements:
            #     vals.append("1.000000")  # amplitude
            #     phase = a.sectors[27].get_phase_for_element(element)
            #     vals.append("{:.6f}".format(phase))
            #     if vals[-1] == "-0.000000":
            #         vals[-1] = "0.000000"
            # f.write(",".join(vals) + "\n")
            ## DONE


            f.write(str(a.sectorCount) + "\n")
            ##DOUBLE QUASI!
            f.write("1\n2\n2\n")
            # phases = prod(antennaSize)* ["0.000000"]
            f.write("1.000000," + ",1.000000,".join(phases) + "\n")

            for sector in a.sectors:
                f.write(str(sector.id) + "\n")
                f.write(str(sector.type) + "\n")
                f.write(str(sector.usage) + "\n")
                vals = []
                for element in a.elements:
                    vals.append("1.000000")# if sector.id == 30 else "0.000000") #amplitude
                    phase = sector.get_phase_for_element(element)
                    vals.append("{:.6f}".format(phase))
                    if vals[-1] == "-0.000000":
                        vals[-1] = "0.000000"
                f.write(",".join(vals) + "\n")

if __name__ == "__main__":
    sectors = 37
    antenna = Antenna(id=1, orientation=(0,0), shape=antennaSize, phaseBits=2, sectorCount=sectors, duplicateElements=False)
    # for i in range(sectors):
    #     sector = Sector(id=i+1, azimuth=round((360 / sectors)*i), elevation=0)
    #     antenna.add_sector(sector)

    #azmths = [45,225,226,227,228,229,230,231,232,233,234,235,236,237,238,239]
    #azmths = list(range(30,361,10)) + list(range(0,30,10))
    azmths = list(range(0,360,10))
    #azmths = [355,356,357,358,359,0,1,2,3,4,5,6,7,8,9,10]
    # azmths = np.array(azmths, dtype=int).tolist()

    azdirs = np.array([-50, -30, -10, 10, 30, 50])
    eldirs = np.array([-50, -30, -10, 10, 30, 50])
    # azdirs = np.array([0,0,0,0,0,0])
    # eldirs = np.array([0,0,0,0,0, 0])
    azdirs = np.repeat(azdirs, 6)
    eldirs = np.tile(eldirs, 6)
    dirs = np.vstack([azdirs, eldirs]).T

    for i in range(sectors-1):
        #Usage 0 is BHI, 1 is SLS, 2 is BOTH
        sector = Sector(id=i + 2, azimuth=dirs[i,0], elevation=dirs[i,1], usage=2)# if i%2==0 else 1)
        # sector = Sector(id=i+2, azimuth=azmths[i], elevation=-45, usage = 2)
        antenna.add_sector(sector)

    write_to_file([antenna])
