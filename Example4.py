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

import numpy as np
from EMPY.Electrostatics.Charge3D import Charge3D
from EMPY.Electrostatics.System3D import ContinuousSystem3D

N=10
L=5e0
R=1.5e0
charge=50
numpts=10000
q = charge / numpts


charges = []

z = np.linspace(0, L, numpts)
theta = 2 * np.pi * N / L * z
x = R * np.cos(theta)
y = R * np.sin(theta)

for i in range(len(z)):
    charges.append(Charge3D(q,[x[i],y[i],0]))

circularLoop = ContinuousSystem3D(charges)
circularLoop.plotField([-6,6],[-6,6],[-6,6], (x,y,np.zeros(len(x))))
