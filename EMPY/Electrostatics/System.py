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

import math
import numpy as np
import matplotlib.pyplot as plt
from EMPY.Electrostatics.Charge import Charge

# A System object to store, keep track, and visualize a list of 2-Dimensional Charge Objects
class System:

    def __init__(self):
        # Initialize an empty list of 2D Charge Objects
        self.chargeLists = []

    # Method to add a single Charge object to chargeLists
    def add_Charge(self, charge):
        self.chargeLists.append(charge)

    # Calculate the total electric field of all Charge Objects present in the System
    def E_Total(self, fieldPos):
        Ex_total, Ey_total = 0, 0
        for C in self.chargeLists:
            Ex_total += Charge.electricField(C, fieldPos)[0]
            Ey_total += Charge.electricField(C, fieldPos)[1]
        return Ex_total, Ey_total

    # Calculate the total electric potential of all Charge Objects present in the System
    def V_Total(self, fieldPos):
        V_Total = 0
        for C in self.chargeLists:
            V_Total += Charge.electricPot(C, fieldPos)
        return V_Total

    # Getter Method for accessing the list of Charge Objects
    def getCharges(self):
        return self.chargeLists

    # Plot the 3D Projection of the total Electric Potential of the combined charge objects in chargeLists.
    def plotPotential3D(self, xs, ys, w):
        width = w
        height = (ys[1] - ys[0]/(xs[1]-xs[0])*width)

        x, y = np.meshgrid(np.linspace(xs[0], xs[1], 500),
                           np.linspace(ys[0], ys[1], 500))
        total_VField = self.V_Total([x,y])
        for i in range(len(total_VField)):
            for j in range(len(total_VField[i])):
                if total_VField[i][j] < 0:
                    total_VField[i][j] = -math.pow(-total_VField[i][j], float(1) / 9)
                else:
                    total_VField[i][j] = total_VField[i][j] ** (1 / 9)
        fig = plt.figure(figsize=(width+2, height+2))
        ax = plt.axes(projection="3d")
        ax = plt.axes(projection="3d")
        ax.set_xlabel("x", fontsize=14)
        ax.set_ylabel("y", fontsize=14)
        ax.set_zlabel("magnitude", fontsize=14)
        # Set spacing b/w the labels and the plot.
        ax.xaxis.labelpad = 10
        ax.yaxis.labelpad = 10
        ax.zaxis.labelpad = 10
        surf = ax.plot_surface(x, y, total_VField, cmap="Spectral", antialiased=True)

        plt.colorbar(surf, shrink=0.8)
        plt.show()


# A DiscreteSystem object to store, keep track, and visualize a list of 2-Dimensional Charge Objects
class DiscreteSystem(System):

    def __init__(self):
        System.__init__(self);

    # Plot the Total Electric Field Generated by all the Charge Objects in chargeLists
    def plot_VectField(self, xs, ys, showEField = True, showEPot = False):
        plt.figure()

        x, y = np.meshgrid(np.linspace(xs[0], xs[1], 100),
                           np.linspace(ys[0], ys[1], 100))

        if showEField:
            Ex, Ey = self.E_Total([x,y])
            P = (Ex ** 2 + Ey ** 2)
            plt.streamplot(x, y, Ex, Ey, color=np.log(P), density=0.9 ,linewidth=2, cmap=plt.cm.get_cmap("Spectral"), arrowsize=2.)
            ax = plt.gca()  # get current axis
            for c in self.getCharges():
                ax.add_patch(plt.Circle((Charge.get_Pos(c)[0], Charge.get_Pos(c)[1]), radius=0.1, color='k', zorder=20))
            ax.set_aspect('equal')
            plt.colorbar()
            plt.draw()

        if showEPot:
            V = self.V_Total([x,y])
            V[V > 10000] = 10000
            plt.contour(x, y, V, 500)

        plt.show()


# A ContinuousSystem object to store, keep track, and visualize a
# continuous distribution of 2-Dimensional Charge Objects.
class ContinuousSystem(System):

    def __init__(self):
        System.__init__(self)

    # Create a Continuous Line Charge Distribution
    def line_charge(self, pX, pY, l, density, Q):
        for qdl in range(int(l*density)):
            qPosition = [pX(qdl/density), pY(qdl/density)]
            charge = Charge(Q/density, qPosition)
            self.add_Charge(charge)

    # Create a Continuous Surface Charge Distribution
    def plate(self, dim, vertex, density, Q):
        sigma = Q / (dim[0]*dim[1]*density**2)
        for i in range(int(dim[0]*density)):
            for j in range(int(dim[1]*density)):
                qPosition = [i/density + vertex[0], j/density + vertex[1]]
                charge = Charge(sigma, qPosition)
                self.add_Charge(charge)

    # Create a Continuous Charge Distribution in the form of a Straight Wire
    def straightWire(self,start, end, res, Q):
        length = ((end[1] - start[1]) ** 2 + (end[0] - start[0]) ** 2) ** 0.5
        gradient = (end[1] - start[1]) / (end[0] - start[0])
        intercept = start[1] - gradient * start[0]

        lambd = Q / length
        for i in range(int((end[0] - start[0]) * res)):
            charge = Charge(lambd, [i / res + start[0], gradient * (i / res) + intercept])
            self.add_Charge(charge)

    # Create a Continuous Charge Distribution in the form of a Circular Loop
    def circularWire(self, center, R, density, Q):
        def x(t):
            return center[0] - R*np.cos(t)
        def y(t):
            return center[1] - R*np.sin(t)
        self.line_charge(pX=x, pY=y, l = 2*np.pi, density=density, Q=Q)

    # Plot the Total Electric Field Generated by the Continuous Charge Distribution in the System.
    def plot_VectField(self, xs, ys, showEField = True, showEPot = False):
        plt.figure()

        x, y = np.meshgrid(np.linspace(xs[0], xs[1], 100),
                           np.linspace(ys[0], ys[1], 100))

        if showEField:
            Ex, Ey = self.E_Total([x,y])
            P = (Ex ** 2 + Ey ** 2)
            plt.streamplot(x, y, Ex, Ey, color=np.log(P), density=0.9 ,linewidth=2, cmap=plt.cm.get_cmap("Spectral"), arrowsize=2.)
            ax = plt.gca()  # get current axis
            for c in self.getCharges():
                ax.add_patch(plt.Circle((Charge.get_Pos(c)[0], Charge.get_Pos(c)[1]), radius=1/len(self.getCharges()), color='k', zorder=20))
            ax.set_aspect('equal')
            plt.colorbar()
            plt.draw()

        if showEPot:
            V = self.V_Total([x,y])
            V[V > 10000] = 10000
            plt.contourf(x, y, V, cmap="coolwarm", alpha=0.6)

        plt.show()

