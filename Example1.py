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
File: Example1.py
Date: 19/10/2019
Description: A class to define an Electrically Charged Point Object.
             Charge object requires input a charge q and its source position.

Usage: Requires math, numpy and matplotlib.pyplot libraries.

This code and Charge library was inspired by Robert Martin's ElectrodynamicsPy Project.
https://github.com/robertmartin8/ElectrodynamicsPy
'''

from EMPY.Electrostatics.Charge import Charge
from EMPY.Electrostatics.System import DiscreteSystem
from EMPY.Electrostatics.System import ContinuousSystem

Q = 1.6e-19
xs = ys = [-1, 1]

#System 1 - Q1 = Q2 = +q
c1 = Charge(1, [-0.3, 0])
c2 = Charge(1, [0.3, 0])

chargeDist1 = DiscreteSystem()
chargeDist1.add_Charge(c1)
chargeDist1.add_Charge(c2)
chargeDist1.plot_VectField(xs=xs, ys=ys,showEField=True, showEPot=False)
chargeDist1.plotPotential3D(xs,ys,6)

#System 2 - Q1 = 4Q2
c1 = Charge(1, [-0.3, 0])
c2 = Charge(4, [0.3, 0])

chargeDist1 = DiscreteSystem()
chargeDist1.add_Charge(c1)
chargeDist1.add_Charge(c2)
chargeDist1.plot_VectField(xs=xs, ys=ys,showEField=True, showEPot=True)
chargeDist1.plotPotential3D(xs,ys,6)

#System 3 - Q1 = -q
pos = [0,0]
c = Charge(-1, pos)

c.plot_VectField(xs=xs, ys=ys,showEField=True, showEPot=True)
c.plotPotential3D([-1, 1],[-1,1],6)


#System 4 - Straight Wire
contSys2 = ContinuousSystem()
contSys2.straightWire([-1, 0], [1, 0], res=80, Q=1*Q)
contSys2.plot_VectField([-2,2],[-2,2], showEField=True, showEPot=True)
contSys2.plotPotential3D([-2,2],[-2,2],6)

#System 5 - Parallel Lines
contSys1 = ContinuousSystem()
contSys1.straightWire([-2, 1], [2, 1], res=80, Q=1*Q)
contSys1.straightWire([-2, -1], [2, -1], res=80, Q=-1*Q)
contSys1.plot_VectField([-4,4],[-4,4], showEField=True, showEPot=True)
contSys1.plotPotential3D([-4,4],[-4,4],6)



#System 6 - Circular Loop
contSys3 = ContinuousSystem()
contSys3.circularWire([0,0], R=1, density=100, Q=100*Q)
contSys3.plot_VectField([-2,2],[-2,2], showEField=True, showEPot=True)
contSys3.plotPotential3D([-2,2],[-2,2],6)

#System 7 - Square Plate
contSys4 = ContinuousSystem()
contSys4.plate([1, 1], [-0.5, -0.5], density=80, Q=100*Q)
contSys4.plot_VectField([-2,2],[-2,2], showEField=True, showEPot=True)
contSys4.plotPotential3D([-2,2],[-2,2],6)