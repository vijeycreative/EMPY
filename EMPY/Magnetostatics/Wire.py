from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np

class Wire(object):
    def __init__(self, r, pos):
        self.r = r
        self.pos = pos
        self.phi = np.linspace(-2 * np.pi, 2 * np.pi, 100)
        self.x = r * np.cos(self.phi) + self.pos[0]
        self.y = r * np.sin(self.phi) + self.pos[1]

    def calculateB(self, x, y):
        i = 1  # Amps in the wire
        mu = 1.26 * 10 ** (-6)  # Magnetic constant
        mag = (mu / (2 * np.pi)) * (i / np.sqrt((x) ** 2 + (y) ** 2))  # Magnitude of the vector B
        by = mag * (np.cos(np.arctan2(y, x)))  # By
        bx = mag * (-np.sin(np.arctan2(y, x)))  # Bx
        return bx, by

    def plotBField2D(self, xs, ys, npts = 10):
        x = np.linspace(xs[0], xs[1], 10)
        y = np.linspace(ys[0], ys[1], 10)
        x, y = np.meshgrid(x, y)
        fig = plt.figure()
        ax = plt.gca()
        bx, by = self.calculateB(x, y)
        P = (bx ** 2 + by ** 2)
        plt.streamplot(x + self.pos[0], y + self.pos[1], bx, by, color=np.log(P), density=0.9, linewidth=2, cmap=plt.cm.get_cmap("Spectral"),
                       arrowsize=2.)
        ax.add_patch(plt.Circle((self.pos[0], self.pos[1]), radius=self.r, color='k', zorder=20))
        plt.colorbar()
        plt.draw()
        plt.show()

    def plotBField3D(self, xs, ys, zs, npts = 10):
        x = np.linspace(xs[0], xs[1], npts)
        y = np.linspace(ys[0], ys[1], npts)
        z = np.linspace(zs[0], zs[1], npts)
        x, y, z = np.meshgrid(x, y, z)
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        bx, by = self.calculateB(x, y)
        bz = 0
        ax.quiver(x + self.pos[0], y + self.pos[1], z, bx, by, bz, cmap='coolwarm', length=0.5, normalize=True)
        for i in np.linspace(zs[0], zs[1], 800):  # Plot the wire
            ax.plot(self.x, self.y, i, label='Cylinder', color='Purple')
        plt.draw()
        plt.show()
