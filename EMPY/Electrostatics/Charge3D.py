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
File: Charge3D.py
Date: 19/10/2019
Description: A class to define an 3 Dimension Electrically Charged Point Object.
             Charge object requires input a charge q and its source position.

Usage: Requires numpy and mayavi libraries.

The use of Mayavi Library for 3 Dimensional Scientific Plotting was inspired from danielsjensen1's electrodynamics project.
https://github.com/danielsjensen1/electrodynamics
'''

from mayavi import mlab
import numpy as np


class Charge3D:

    def __init__(self, q, sourcePos):
        self.q = q
        self.pos = sourcePos

    def getCharge(self):
        return self.q

    def getPosition(self):
        return self.pos

        # Determine Analytical Electric Field of Point Charge at a given position vector fieldPos.

    def electricField(self, fieldPos):
        # Separation Vector r - Griffith Page 9, Eqn 27
        r = np.sqrt((fieldPos[0] - self.pos[0]) ** 2 + (fieldPos[1] - self.pos[1]) ** 2 + (fieldPos[2]-self.pos[2])**2)
        # Setting tolerance for separation vector.
        r[r < 0.005] = 0.005
        # The x and y component of Electric Field E - Griffith Page 61, Eqn 4
        Ex = self.q * (fieldPos[0] - self.pos[0]) / (r ** 3)
        Ey = self.q * (fieldPos[1] - self.pos[1]) / (r ** 3)
        Ez = self.q * (fieldPos[2] - self.pos[2]) / (r ** 3)
        return Ex, Ey, Ez

    def potentialField(self, fieldPos):
        # Separation Vector r - Griffith Page 9, Eqn 27
        r = np.sqrt((fieldPos[0] - self.pos[0]) ** 2 + (fieldPos[1] - self.pos[1]) ** 2 + (fieldPos[2]-self.pos[2])**2)
        # Setting tolerance for separation vector.
        r[r < 0.005] = 0.005
        # Potential of Point Charge - Griffith Page 85, Eqn 26
        V = self.q / r
        return V

    def plotField(self, xs, ys, zs):
        x, y, z = np.mgrid[xs[0]:xs[1]:10j, ys[0]:ys[1]:10j, zs[0]:zs[1]:10j]

        Ex, Ey, Ez = self.electricField([x,y,z])

        if self.getCharge() < 0:
            color = (0,0,1)
        else:
            color = (1,0,0)
        mlab.figure(size=(1000,1000))
        mlab.points3d(self.getPosition()[0], self.getPosition()[1], self.getPosition()[2], color=color, scale_factor = 1)
        mlab.quiver3d(x,y,z, Ex, Ey, Ez, line_width = 2, scale_factor = 1)

        mlab.show()


