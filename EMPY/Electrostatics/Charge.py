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
File: Charge.py
Date: 19/10/2019
Description: A class to define an Electrically Charged Point Object.
             Charge object requires input a charge q and its source position.

Usage: Requires math, numpy and matplotlib.pyplot libraries.

This code and Charge library was inspired by Robert Martin's ElectrodynamicsPy Project.
https://github.com/robertmartin8/ElectrodynamicsPy
'''
import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class Charge:
    'A Charge Object to be constituting of a q coulomb charge, and a source point vector r.'

    # A constructor for a simple point charge.
    def __init__(self, q, sourcePos):
        self.q = q
        self.pos = sourcePos

    def get_Pos(self):
        return self.pos

    # Determine Analytical Electric Field of Point Charge at a given position vector fieldPos.
    def electricField(self, fieldPos):
        # Separation Vector r - Griffith Page 9, Eqn 27
        r = np.sqrt((fieldPos[0] - self.pos[0])**2 + (fieldPos[1]-self.pos[1])**2)
        # Setting tolerance for separation vector.
        r[r < 0.005] = 0.005
        # The x and y component of Electric Field E - Griffith Page 61, Eqn 4
        Ex = self.q * (fieldPos[0] - self.pos[0])/(r**3)
        Ey = self.q * (fieldPos[1] - self.pos[1]) / (r**3)
        return Ex, Ey

    # Determine Analytical Electric Potential at a given position vector fieldPos.
    def electricPot(self, fieldPos):
        # Separation Vector r - Griffith Page 9, Eqn 27
        r = np.sqrt((fieldPos[0] - self.pos[0]) ** 2 + (fieldPos[1] - self.pos[1]) ** 2)
        # Setting tolerance for separation vector.
        r[r < 0.005] = 0.005
        # Potential of Point Charge - Griffith Page 85, Eqn 26
        V = self.q/r
        return V

    # Plot the Electric Field Generated by the Charge Object
    def plot_VectField(self, xs, ys, showEField = True, showEPot = False):
        plt.figure()

        x, y = np.meshgrid(np.linspace(xs[0], xs[1], 100),
                           np.linspace(ys[0], ys[1], 100))

        if showEField:
            Ex, Ey = self.electricField([x,y])
            P = (Ex ** 2 + Ey ** 2)
            plt.streamplot(x, y, Ex, Ey, color=np.log(P), density=0.9 ,linewidth=2, cmap=plt.cm.get_cmap("Spectral"), arrowsize=2.)
            ax = plt.gca()  # get current axis
            ax.add_patch(plt.Circle((self.pos[0], self.pos[1]), radius=0.1, color='k', zorder=20))
            ax.set_aspect('equal')
            plt.colorbar()
            plt.draw()

        if showEPot:
            V = self.electricPot([x,y])
            V[V > 10000] = 10000
            plt.contour(x, y, V,250)

        plt.show()

    # Draw a 3D Projection of the Charge Object's Electric Potential
    def plotPotential3D(self, xs, ys, w):
        width = w
        height = (ys[1] - ys[0]/(xs[1]-xs[0])*width)

        x, y = np.meshgrid(np.linspace(xs[0], xs[1], 500),
                           np.linspace(ys[0], ys[1], 500))
        total_VField = self.electricPot([x,y])
        for i in range(len(total_VField)):
            for j in range(len(total_VField[i])):
                if total_VField[i][j] < 0:
                    total_VField[i][j] = -math.pow(-total_VField[i][j], float(1) / 9)
                else:
                    total_VField[i][j] = total_VField[i][j] ** (1 / 9)
        fig = plt.figure(figsize=(width, height))
        ax = plt.axes(projection="3d")
        ax.set_xlabel("x", fontsize=14)
        ax.set_ylabel("y", fontsize=14)
        ax.set_zlabel("magnitude", fontsize=14)
        # Set spacing b/w the labels and the plot.
        ax.xaxis.labelpad = 10
        ax.yaxis.labelpad = 10
        ax.zaxis.labelpad = 10
        surf =ax.plot_surface(x, y,
                        total_VField,
                        cmap="Spectral", antialiased=True)

        plt.colorbar(surf, shrink=0.8)
        plt.show()