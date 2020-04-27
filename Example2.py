'''
__/\\\\\\\\\\\\\\\_        __/\\\\____________/\\\\_        __/\\\\\\\\\\\\\___        __/\\\________/\\\_
 _\/\\\///////////__        _\/\\\\\\________/\\\\\\_        _\/\\\/////////\\\_        _\///\\\____/\\\/__
  _\/\\\_____________        _\/\\\//\\\____/\\\//\\\_        _\/\\\_______\/\\\_        ___\///\\\/\\\/____
   _\/\\\\\\\\\\\_____        _\/\\\\///\\\/\\\/_\/\\\_        _\/\\\\\\\\\\\\\/__        _____\///\\\/______
    _\/\\\///////______        _\/\\\__\///\\\/___\/\\\_        _\/\\\/////////____        _______\/\\\_______
     _\/\\\_____________        _\/\\\____\///_____\/\\\_        _\/\\\_____________        _______\/\\\_______
      _\/\\\_____________        _\/\\\_____________\/\\\_        _\/\\\_____________        _______\/\\\_______
       _\/\\\\\\\\\\\\\\\_        _\/\\\_____________\/\\\_        _\/\\\_____________        _______\/\\\_______
        _\///////////////__        _\///______________\///__        _\///______________        _______\///________

    ________          __                                              __  _         ____        __  __
   / ____/ ___  _____/ /__________  ____ ___  ____ _____ _____  ___  / /_(______   / __ \__  __/ /_/ /_  ____  ____
  / __/ / / _ \/ ___/ __/ ___/ __ \/ __ `__ \/ __ `/ __ `/ __ \/ _ \/ __/ / ___/  / /_/ / / / / __/ __ \/ __ \/ __ \
 / /___/ /  __/ /__/ /_/ /  / /_/ / / / / / / /_/ / /_/ / / / /  __/ /_/ / /__   / ____/ /_/ / /_/ / / / /_/ / / / /
/_____/_/\___/\___/\__/_/   \____/_/ /_/ /_/\__,_/\__, /_/ /_/\___/\__/_/\___/  /_/    \__, /\__/_/ /_/\____/_/ /_/
                                                 /____/                               /____/

Author: V Vijendran
File: System.py
Date: 19/10/2019
Description: Contains System, DiscreteSystem(System) and ContinuousSystem(System) Classes.
             System object stores and keeps track of list of charges in a given setting.
             DiscreteSystem is child class of System which is used for system of discrete charges.
             ContinuousSystem is child class of System which is used for system of continuous charges.

             System object requires input a charge to be initialized.

Usage: Requires math, numpy, matplotlib.pyplot libraries, and EMPY.Electrostatics.Charge.

This code and Charge library was inspired by Robert Martin's ElectrodynamicsPy Project.
https://github.com/robertmartin8/ElectrodynamicsPy
'''


from EMPY.Electrostatics.System3D import DiscreteSystem3D
from EMPY.Electrostatics.Charge3D import Charge3D

# 3D Plot of Electric Field of a Point Charge
charge3d = Charge3D(1, (0,0,1))
charge3d.plotField([-5,5],[-5,5],[-5,5])

# 3D Plot of Electric Field of a Dipole
charge3d_01 = Charge3D(-1, (-2,0,0))
charge3d_02 = Charge3D(1, (2,0,0))
discreteSys_01 = DiscreteSystem3D([charge3d_01, charge3d_02])
discreteSys_01.plotField([-5,5],[-5,5],[-5,5])

# Create a Infinitesimal Line Charge consisting of 5 3D Charge Objects
charge3d_03 = Charge3D(1, (-2,0,0))
charge3d_04 = Charge3D(1, (-1,0,0))
charge3d_05 = Charge3D(1, (0,0,0))
charge3d_06 = Charge3D(1, (1,0,0))
charge3d_07 = Charge3D(1, (2,0,0))
discreteSys_02 = DiscreteSystem3D([charge3d_03,charge3d_04,charge3d_05,charge3d_06,charge3d_07])
discreteSys_02.plotField([-5,5],[-5,5],[-5,5])

# Create a Singe Plate in a Discrete Charge System
z0=0e0
dz0=2e0
charge0=10e0
numpts0 = 9e0
q0 = charge0 / numpts0
charges0 = []
for x in range(-3,4):
    for y in range(-3,4):
        charges0.append(Charge3D(q0, (x, y, z0)))
parallelPlate = DiscreteSystem3D(charges0)
parallelPlate.plotField([-5,5],[-5,5],[-5,5])

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
