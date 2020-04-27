import math
from EMPY.Magnetostatics import Loops

# Maxwell coil model with single current loops

R = 10

# center winding
c1 = Loops.Loop([0, 0, 0], [1, 0, 0], R, 64)

# outer windings
c2 = Loops.Loop([-R*math.sqrt(3./7.), 0, 0], [1, 0, 0], R*math.sqrt(4./7.), 49)
c3 = Loops.Loop([+R*math.sqrt(3./7.), 0, 0], [1, 0, 0], R*math.sqrt(4./7.), 49)


cSystem = Loops.LoopSystem()
cSystem.addLoop(c1)
cSystem.addLoop(c2)
cSystem.addLoop(c3)
cSystem.plotBField(-15, 15, 101, -15, 15, 101)