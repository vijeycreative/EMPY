import math
import numpy as np
import scipy.special
import matplotlib.pyplot as plt

def normalize(v):
  l = np.linalg.norm(v)
  epsilon = 1e-9
  if l < epsilon:
    raise ValueError("Vector with |v| < e normalized")
  return v / l

class Loop(object):
  def __init__(self, position, normal, radius, current):
    self.p = np.array(position, dtype = np.float64)
    self.n = normalize(np.array(normal, dtype = np.float64))
    self.r = np.float64(radius)
    self.i = np.float64(current)

class LoopSystem(object):
  def __init__(self,
               length_units = 1,
               current_units = 1,
               field_units = 1):
    self.loops = []
    self._length_units = length_units
    self._field_units = field_units
    self._epsilon = np.finfo(np.float64).eps

  def addLoop(self, loop):
      self.loops.append(loop)

  def evaluate(self, position):
      _p = np.atleast_2d(position)
      B = np.zeros(_p.shape)
      for loop in self.loops:
          B += self._evalLoop(_p, loop)
      return np.squeeze(B / self._field_units)

  def _evalLoop(self, p, loop):
      r_vect = (p - loop.p) * self._length_units
      r = np.linalg.norm(r_vect, axis=1, keepdims=True)
      z = r_vect.dot(loop.n.T)
      rho_vect = r_vect - np.outer(z, loop.n)
      rho = np.linalg.norm(rho_vect, axis=1)
      rho_vect[rho > self._epsilon,] = \
          (rho_vect[rho > self._epsilon,].T / rho[rho > self._epsilon]).T

      a = loop.r * self._length_units
      alpha2 = a * a + rho * rho + z * z - 2. * a * rho
      beta2 = a * a + rho * rho + z * z + 2. * a * rho
      beta = np.sqrt(beta2)
      c = 4.e-7 * loop.i  # \mu_0  I / \pi
      a2b2 = alpha2 / beta2
      Ek2 = scipy.special.ellipe(1. - a2b2)
      Kk2 = scipy.special.ellipkm1(a2b2)

      denom = (2. * alpha2 * beta * rho)
      with np.errstate(invalid='ignore'):
          numer = c * z * ((a * a + rho * rho + z * z) * Ek2 - alpha2 * Kk2)
      sw = np.abs(denom) > self._epsilon
      Brho = np.zeros(numer.shape)
      Brho[sw] = numer[sw] / denom[sw]

      denom = (2. * alpha2 * beta)
      with np.errstate(invalid='ignore'):
          numer = c * ((a * a - rho * rho - z * z) * Ek2 + alpha2 * Kk2)
      sw = np.abs(denom) > self._epsilon
      Bz = np.full(numer.shape, np.inf)
      Bz[sw] = numer[sw] / denom[sw]

      return (Brho * rho_vect.T).T + np.outer(Bz, loop.n)

  def plotBField(self, min_x, max_x, n_x, min_y, max_y, n_y, n_lines = None, density = None):
      X = np.linspace(min_x, max_x, n_x)
      Y = np.linspace(min_y, max_y, n_y)
      points = np.empty([n_y * n_x, 3])
      for i in range(0, n_y):
          for j in range(0, n_x):
              points[n_x * i + j, :] = np.array([X[j], Y[i], 0.])
      B = self.evaluate(points)
      legend_handles = []
      if n_lines is None:
          n_lines = math.floor(n_x / 2)
      if density is None:
          density = 10
      start_points = (
          np.array([np.zeros(n_lines),
                    min_y + (max_y - min_y) *
                    (0.5 + np.linspace(0, n_lines - 1, n_lines)) /
                    (n_lines)]).transpose())
      Bx = np.reshape(B[:, 0], [n_y, n_x])
      By = np.reshape(B[:, 1], [n_y, n_x])
      P = (Bx ** 2 + By ** 2)
      plt.streamplot(X, Y,
                            Bx,
                            By,
                            linewidth=1, density=density,
                            color=np.log(P),
                            arrowsize=1.,
                            cmap=plt.cm.get_cmap("Spectral"),
                            start_points=start_points)
      scale = 1
      for loop in self.loops:
          dp = loop.r * np.array([loop.n[1], -loop.n[0], 0])
          p0 = loop.p - dp
          pos_X = (p0[0])
          pos_Y = (p0[1])
          p1 = loop.p + dp
          neg_X = (p1[0])
          neg_Y = (p1[1])

          plt.plot(pos_X, pos_Y, 'o', fillstyle='none',
                   linewidth=3 * scale, markersize=20 * scale,
                   color='black', markeredgewidth=3 * scale)
          plt.plot(pos_X, pos_Y, 'o', fillstyle='full',
                   linewidth=3 * scale, markersize=7 * scale,
                   color='black', markeredgewidth=1 * scale)
          plt.plot(neg_X, neg_Y, 'o', fillstyle='none',
                   linewidth=3 * scale, markersize=20 * scale,
                   color='black', markeredgewidth=3 * scale)
          plt.plot(neg_X, neg_Y, 'x', fillstyle='none',
                   linewidth=3 * scale, markersize=9 * scale,
                   color='black', markeredgewidth=3 * scale)
      plt.legend(handles=legend_handles)
      plt.show()