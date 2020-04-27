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
File: System3D.py
Date: 19/10/2019
Description: Contains System3D, DiscreteSystem3D(System) and ContinuousSystem3D(System) Classes.
             System3D object stores and keeps track of list of 3D charges in a given setting.
             DiscreteSystem3D is child class of System which is used for system of discrete charges.
             ContinuousSystem3D is child class of System which is used for system of continuous charges.

             System3D object requires input a charge to be initialized.

Usage: Requires math, numpy, mayavi libraries, and EMPY.Electrostatics.Charge3D.

The use of Mayavi Library for 3 Dimensional Scientific Plotting was inspired from danielsjensen1's electrodynamics project.
https://github.com/danielsjensen1/electrodynamics
'''

from mayavi import mlab
import numpy as np
from EMPY.Electrostatics.Charge3D import Charge3D


def addUniqueSource(source, sourceList):
    import warnings
    if source not in sourceList:
        sourceList += [source]
    else:
        warnings.warn("Source " + str(source) +
                      " already in Collection list; Ignoring", Warning)


def addListToCollection(sourceList, inputList, dupWarning):
    if dupWarning is True:  # Skip iterating both lists if warnings are off
        for source in inputList:
            # Checks if source is in list, throw warning
            addUniqueSource(source, sourceList)
    else:
        sourceList.extend(inputList)


# A System3D object to store, keep track, and visualize a list of 3-Dimensional Charge3D Objects
class System3D:

    def __init__(self, sources, dupWarning=True):
        # Initialize an empty list of Charge3D Objects
        self.charge3DLists = []

        for s in sources:
            if type(s) == System3D:
                addListToCollection(self.charge3DLists, s.charge3DLists, dupWarning)
            elif isinstance(s, list) or isinstance(s, tuple):
                addListToCollection(self.charge3DLists, s, dupWarning)
            else:
                if dupWarning is True:
                    addUniqueSource(s, self.charge3DLists)
                else:
                    self.charge3DLists += [s]

    def get_Charge3DList(self):
        return self.charge3DLists

    # Method to add a single Charge3D object to charge3DLists
    def add_Charge3D(self, charge3D):
        self.charge3DLists.append(charge3D)

    # Calculate the total electric field of all Charge3D Objects present in the System3D
    def E_Total(self, fieldPos):
        Ex_total, Ey_total, Ez_total = 0, 0, 0

        for C in self.get_Charge3DList():
            Ex_total += Charge3D.electricField(C, fieldPos)[0]
            Ey_total += Charge3D.electricField(C, fieldPos)[1]
            Ez_total += Charge3D.electricField(C, fieldPos)[2]

        return Ex_total, Ey_total, Ez_total

    # Calculate the total electric potential of all Charge3D Objects present in the System3D
    def V_Total(self, fieldPos):
        V_Total = 0
        for C in self.get_Charge3DList():
            V_Total += Charge3D.potentialField(C, fieldPos)
        return V_Total


# A DiscreteSystem3D object to store, keep track, and visualize a discrete distribution of
# 3-Dimensional Charge3D Objects contained in the system.
class DiscreteSystem3D(System3D):

    def __init__(self, sources, dupWarning=True):
        System3D.__init__(self, sources, dupWarning)

    # Plot the Total Electric Field Generated by all the Charge3D Objects in charge3DLists
    def plotField(self, xs, ys, zs):
        x, y, z = np.mgrid[xs[0]:xs[1]:10j, ys[0]:ys[1]:10j, zs[0]:zs[1]:10j]

        Ex, Ey, Ez = self.E_Total([x,y,z])

        mlab.figure(size=(1000,1000))
        for C in self.get_Charge3DList():
            if Charge3D.getCharge(C) < 0:
                color = (0, 0, 1)
            else:
                color = (1, 0, 0)
            mlab.points3d(Charge3D.getPosition(C)[0], Charge3D.getPosition(C)[1], Charge3D.getPosition(C)[2], color=color, scale_factor = 1)
        mlab.quiver3d(x,y,z, Ex, Ey, Ez, line_width=2, scale_factor=1, colormap='gist_rainbow', opacity=0.6)
        mlab.show()


# A ContinuousSystem3D object to store, keep track, and visualize a
# continuous distribution of 3-Dimensional Charge3D Objects.
class ContinuousSystem3D(System3D):

    def __init__(self, sources, dupWarning=True):
        System3D.__init__(self, sources, dupWarning)

    # Plot the Total Electric Field Generated by the Continuous Charge3D Distribution in the System.
    def plotField(self, xs, ys, zs, object):
        x, y, z = np.mgrid[xs[0]:xs[1]:10j, ys[0]:ys[1]:10j, zs[0]:zs[1]:10j]

        Ex, Ey, Ez = self.E_Total([x,y,z])

        mlab.figure(size=(1000,1000))
        mlab.plot3d(object[0], object[1], object[2], tube_radius=0.15, colormap='Spectral')
        mlab.quiver3d(x,y,z, Ex, Ey, Ez, line_width=1, scale_factor=1, colormap='gist_rainbow', opacity=0.75)
        mlab.show()