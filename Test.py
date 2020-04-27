from EMPY.Electrostatics.System3D import DiscreteSystem3D
from EMPY.Electrostatics.Charge3D import Charge3D

# Create a Parallel Plate Capacitor in a Discrete Charge System
z=0e0
dz=2e0
charge=10e0
numpts = 9e0
q = charge / numpts
charges = []
for x in range(-3,4):
    for y in range(-3,4):
        charges.append(Charge3D(q, (x, y, z + dz)))
        charges.append(Charge3D(-q, (x, y, z - dz)))
parallelPlate = DiscreteSystem3D(charges)
parallelPlate.plotField([-5,5],[-5,5],[-5,5])