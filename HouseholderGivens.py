import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from mpl_toolkits.mplot3d import Axes3D



def householder(x, k):
    v = x-np.linalg.norm(x)*np.eye(n)[:,k]
    p = x-2*v*np.dot(x,v)/np.linalg.norm(v)**2
    return v, p



def householder2D(x):
    k = int(input('k (0 or 1): '))
    v, p = householder(x, k)

    if x[0]>p[0]: 
        angle = np.pi/2
    else: 
        angle = -np.pi/2
    vpx = v[0]*np.cos(angle)-v[1]*np.sin(angle)
    vpy = v[0]*np.sin(angle)+v[1]*np.cos(angle)

    plt.quiver(x[0], x[1], angles='xy', scale_units='xy', scale=1, zorder=2, color='b', label='x')
    plt.quiver(p[0], p[1], angles='xy', scale_units='xy', scale=1, zorder=2, color='r', label='x\'')
    plt.quiver(v[0], v[1], angles='xy', scale_units='xy', scale=1, zorder=2, color='g', label='v')
    plt.quiver(vpx, vpy, angles='xy', scale_units='xy', scale=1, color='m', label=r'v$\perp$')

    plotSettings2D()



def householder3D(x):
    k = int(input('k (0 or 1 or 2): '))
    v, p = householder(x, k)

    xx = np.linspace(-3, 3, 5)
    yy = np.linspace(-3, 3, 5)
    xx, yy = np.meshgrid(xx,yy)
    zz = (-v[0]*xx-v[1]*yy)/v[2]

    fig = plt.figure()
    ax = fig.gca(projection='3d')

    ax.quiver(0, 0, 0, x[0], x[1], x[2], color='b', label='x')
    ax.quiver(0, 0, 0, p[0], p[1], p[2], color='r', label='x\'')
    ax.quiver(0, 0, 0, v[0], v[1], v[2], color='g', label='v')
    ax.plot_wireframe(xx, yy, zz, color='m', label=r'v$\perp$')

    plotSettings3D()



def givens(x, i, k):
    angle = float(input('Rotation angle: '))*np.pi/180
    c = np.cos(angle)
    s = np.sin(angle)

    j = np.eye(n)
    j[i,i] = c
    j[i,k] = -s
    j[k,i] = s
    j[k,k] = c

    return np.dot(j,x)



def givens2D(x):
    g = givens(x, 0, 1)

    plt.quiver(x[0], x[1], angles='xy', scale_units='xy', scale=1, zorder=2, color='b', label='x')
    plt.quiver(g[0], g[1], angles='xy', scale_units='xy', scale=1, zorder=2, color='r', label='x\'')

    plotSettings2D()



def givens3D(x):
    k = int(input('k (2 or 3): '))
    if k==2:
        g = givens(x, 0, 1)
    if k==3:
        g = givens(x, 1, 2)

    fig = plt.figure()
    ax = fig.gca(projection='3d')

    ax.quiver(0, 0, 0, x[0], x[1], x[2], color='b', label='x')
    ax.quiver(0, 0, 0, g[0], g[1], g[2], color='r', label='x\'')

    plotSettings3D()



def plotSettings2D():
    plt.xlim(-10, 10)
    plt.ylim(-10, 10)

    plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(1))
    plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(1))
    plt.gca().set_axisbelow(True)
    plt.grid()

    plt.axvline(x=0, zorder=1, color='k')
    plt.axhline(y=0, zorder=1, color='k')

    plt.gca().set_aspect('equal')

    plt.legend(loc="upper right")

    plt.show()



def plotSettings3D():
    plt.gca().set_xlim3d(-10, 10)
    plt.gca().set_ylim3d(-10, 10)
    plt.gca().set_zlim3d(-10, 10)

    plt.legend(loc="upper right")

    plt.show()



algorithm = input('Press H for Householder or G for Givens: ')
n = int(input('n (2 or 3): '))
x = [int(i) for i in input('x ('+str(n)+' numbers): ').split()]

if (algorithm=='H' or algorithm=='h') and n==2:
    householder2D(x)

if (algorithm=='H' or algorithm=='h') and n==3:
    householder3D(x)

if (algorithm=='G' or algorithm=='g') and n==2:
    givens2D(x)

if (algorithm=='G' or algorithm=='g') and n==3:
    givens3D(x)
