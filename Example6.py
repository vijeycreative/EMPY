from EMPY.Magnetostatics import Loops

# single-turn 10 cm x-oriented coil at origin
position = [0., 0., 0.]
normal = [1., 0., 0.]
radius = 10.
current = 1

coil = Loops.Loop(position, normal, radius, current)
cSystem = Loops.LoopSystem()
cSystem.addLoop(coil)

cSystem.plotBField(-15, 15, 101, -15, 15, 101)