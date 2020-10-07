from math import sin, cos, pi, prod
import numpy as np
filename = "codebook"
antennaCount = 1
azimuthsCount = 361
elevationsCount = 181
cardinality_multiplier = 10
cardinality_multiplier_elev = 1

#lambd = 1/60000000.

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
                for y in range(shape[1]):
                    self.elements.append(Element(x, y))
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
        return - pi * get_offset(element, self.azimuth, self.elevation)


def get_offset(element, azimuth, elevation):
    #assert type(azimuth) == type(elevation) == int
    #return sin(azimuth) * (cos(elevation) * element.x_index + sin(elevation)*element.y_index)
    return ( - element.x_index * sin(rad(azimuth)) * cos(rad(elevation)) + element.y_index * sin(rad(elevation)))

def rad(degree):
    return degree / 180. * pi

def azrange():
   return np.linspace(0, azimuthsCount - 1, cardinality_multiplier * (azimuthsCount - 1) + 1)
def elrange():
   return np.linspace(0, elevationsCount - 1, cardinality_multiplier_elev * (elevationsCount - 1) + 1)

def write_to_file(antennas):
    with open(filename, "w") as f:
        f.write(str(len(antennas)) + '\n')
        for a in antennas:
            f.write(str(a.id) + "\n")
            f.write(str(a.orientation[0]) + "\n")
            f.write(str(a.orientation[1]) + "\n")
            f.write(str(a.elementCount) + "\n")
            f.write(str(a.phaseBits) + "\n")
            f.write(str(a.amplitudeBits) + "\n")
            # Directivity (i.e. gain)
            directivityString = ",".join((cardinality_multiplier_elev * (elevationsCount - 1) + 1) * ["1.000000"]) + "\n"
            #for _ in range(azimuthsCount):
            for _ in azrange():
                f.write(directivityString)
            for e in a.elements:
                for az in azrange():
                #for az in range(azimuthsCount):
                    vals = []
                    testidx = 0
                    for el in elrange():
                    #for el in range(elevationsCount):
                        el -= 90
                        testidx += 1
                        vals.append("1.000000")
                        phase = pi * get_offset(element=e, azimuth=az, elevation=el)
                        vals.append("{:.6f}".format(phase))
                    f.write(",".join(vals) + "\n")

            #QuasiOmni AWV
            f.write(",".join(a.elementCount*["1.000000,0.000000"]) + "\n")
            f.write(str(a.sectorCount) + "\n")
            for sector in a.sectors:
                f.write(str(sector.id) + "\n")
                f.write(str(sector.type) + "\n")
                f.write(str(sector.usage) + "\n")
                vals = []
                for element in a.elements:
                    vals.append("1.000000") #amplitude
                    phase = sector.get_phase_for_element(element)
                    vals.append("{:.6f}".format(phase))
                f.write(",".join(vals) + "\n")

sectors = 2
antenna = Antenna(id=1, orientation=(0,0), shape=(32,2), phaseBits=5, sectorCount=sectors, duplicateElements=False)
# for i in range(sectors):
#     sector = Sector(id=i+1, azimuth=round((360 / sectors)*i), elevation=0)
#     antenna.add_sector(sector)

#azmths = [45,225,226,227,228,229,230,231,232,233,234,235,236,237,238,239]
azmths = [69,0]#,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
#azmths = [355,356,357,358,359,0,1,2,3,4,5,6,7,8,9,10]
azmths = np.array(azmths, dtype=np.int).tolist()
for i in range(sectors):
    sector = Sector(id=i+1, azimuth=azmths[i], elevation=0)
    antenna.add_sector(sector)

# sector = Sector(id=1, azimuth=45, elevation=45)
# antenna.add_sector(sector)
# sector = Sector(id=2, azimuth=-45, elevation=-45)
# antenna.add_sector(sector)
write_to_file([antenna])