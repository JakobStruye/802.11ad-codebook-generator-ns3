from math import pi, prod
import numpy as np
filename = "codebookSmart"
antennaCount = 1

class Complex:
    def __init__(self, *, amplitude, phase):
        self.amplitude = amplitude
        self.phase = phase

    def quantize(self, *, amplitudeBits, phaseBits):
        pass

class Antenna:
    def __init__(self, *, id, orientation=(0,0), shape, phaseBits, amplitudeBits=1):
        self.id = id
        self.orientation = orientation
        self.shape = shape
        self.elementCount = prod(shape)
        self.phaseBits = phaseBits
        self.amplitudeBits = amplitudeBits
        self.directivity = None

        self.elements = []
        if not type(shape) == tuple:
            shape = (shape, 1)
        for x in range(shape[0]):
            for y in range(shape[1]):
                self.elements.append(Element(x, y))

class Element:
    def __init__(self, x_index, y_index ):
        self.x_index = x_index
        self.y_index = y_index

def rad(degree):
    return degree / 180. * pi

def write_to_file(antennas):
    with open(filename, "w") as f:
        f.write(str(len(antennas)) + '\n')
        for a in antennas:
            f.write(str(a.id) + "\n")
            f.write(str(a.orientation[0]) + "\n")
            f.write(str(a.orientation[1]) + "\n")
            for shape_val in a.shape:
                f.write(str(shape_val) + "\n")
            f.write(str(a.phaseBits) + "\n")
            f.write(str(a.amplitudeBits) + "\n")
            f.write("0\n") # No directivity

            #QuasiOmni AWV
            f.write(",".join(a.elementCount*["1.000000,0.000000"]) + "\n")


antenna = Antenna(id=1, orientation=(0,0), shape=(8,2), phaseBits=5)
write_to_file([antenna])