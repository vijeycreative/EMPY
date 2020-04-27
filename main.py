


import numpy as np
import  EMPY.Magnetostatics.MagneticElements as MagneticElements
from EMPY.Magnetostatics.MSystem import MSystem


coil1a = [MagneticElements.Circular(curr=1, dim=3, pos=[0, 0, z]) for z in np.linspace(-3, -1, 20)]
c1 = MSystem(coil1a)

c1.displaySystem([-4,3,20])
