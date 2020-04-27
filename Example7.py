from EMPY.Magnetostatics import Loops

# single-turn 10 cm x-oriented coil at origin
# Helmholtz coil model with single current loops
R = 10.

# 2 windings
c1 = Loops.Loop([-R/2., 0, 0], [1, 0, 0], R, 1)
c2 = Loops.Loop([+R/2., 0, 0], [1, 0, 0], R, 1)


cSystem = Loops.LoopSystem()
cSystem.addLoop(c1)
cSystem.addLoop(c2)
cSystem.plotBField(-15, 15, 101, -15, 15, 101)