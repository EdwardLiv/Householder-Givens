import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.widgets import Slider, Button
from mpl_toolkits.mplot3d import Axes3D



def householder(x, k):
    for i in range(len(x)):
        if x[i]==0:
            x[i]=0.01

    v = x-np.linalg.norm(x)*np.eye(len(x))[:,int(k)]
    p = x-2*v*np.dot(x,v)/np.linalg.norm(v)**2

    if (k==0 and x[1]<0) or (k==1 and x[0]>0): 
        angle = 90
    else: 
        angle = -90
    vp = givens(v, 0, 1, angle)

    return p, v, vp



def givens(x, i, k, angle):
    angle = float(angle)*np.pi/180
    c = np.cos(angle)
    s = np.sin(angle)

    j = np.eye(len(x))
    j[i,i] = c
    j[i,k] = -s
    j[k,i] = s
    j[k,k] = c

    return np.dot(j,x)



def householder2D():
    fig, ax = plt.subplots()
    fig.canvas.set_window_title('Householder 2D')
    plt.subplots_adjust(left=0.1, bottom=0.25, right=0.7)
    plotSettings2D()

    def update(val):
        x = [sliderX1.val, sliderX2.val]
        k = sliderK.val
        p, v, vp = householder(x, k)

        try:
            ax.lines.remove([line for line in ax.lines if line.get_label()=='x'][0])
            ax.lines.remove([line for line in ax.lines if line.get_label()=='x\''][0])
            ax.lines.remove([line for line in ax.lines if line.get_label()=='v'][0])
            ax.lines.remove([line for line in ax.lines if line.get_label()==r'v$\perp$'][0])
        except IndexError:
            pass

        plotX, = ax.plot([0, x[0]], [0, x[1]], zorder=2, color='b', label='x')
        plotP, = ax.plot([0, p[0]], [0, p[1]], zorder=2, color='r', label='x\'')
        plotV, = ax.plot([0, v[0]], [0, v[1]], zorder=2, color='g', label='v')
        plotVP, = ax.plot([0, vp[0]], [0, vp[1]], zorder=2, color='m', label=r'v$\perp$')

        ax.legend(loc="upper right")
        plt.draw()

    def onClick(event):
        clickX, clickY = event.xdata, event.ydata
        sliderX1.set_val(clickX)
        sliderX2.set_val(clickY)

    fig.canvas.mpl_connect('button_press_event', onClick)

    axesSliderX1 = plt.axes([0.1, 0.15, 0.8, 0.025])
    sliderX1 = Slider(axesSliderX1, r'$x_1$', valmin=-10, valmax=10, valinit=0)
    axesSliderX2 = plt.axes([0.1, 0.1, 0.8, 0.025])
    sliderX2 = Slider(axesSliderX2, r'$x_2$', valmin=-10, valmax=10, valinit=0)
    axesSliderK = plt.axes([0.1, 0.05, 0.8, 0.025])
    sliderK = Slider(axesSliderK, 'k', valmin=0, valmax=1, valinit=0, valstep=1)

    sliderX1.on_changed(update)
    sliderX2.on_changed(update)
    sliderK.on_changed(update)

    axesButtonHouseholder2D = plt.axes([0.7, 0.8, 0.2, 0.05])
    buttonHouseholder2D = Button(axesButtonHouseholder2D, 'Householder 2D')
    axesButtonHouseholder3D = plt.axes([0.7, 0.7, 0.2, 0.05])
    buttonHouseholder3D = Button(axesButtonHouseholder3D, 'Householder 3D')
    axesButtonGivens2D = plt.axes([0.7, 0.6, 0.2, 0.05])
    buttonGivens2D = Button(axesButtonGivens2D, 'Givens 2D')
    axesButtonGivens3D = plt.axes([0.7, 0.5, 0.2, 0.05])
    buttonGivens3D = Button(axesButtonGivens3D, 'Givens 3D')

    def openHouseholder2D(event):
        plt.close()
        householder2D()

    def openHouseholder3D(event):
        plt.close()
        householder3D()

    def openGivens2D(event):
        plt.close()
        givens2D()

    def openGivens3D(event):
        plt.close()
        givens3D()

    buttonHouseholder2D.on_clicked(openHouseholder2D)
    buttonHouseholder3D.on_clicked(openHouseholder3D)
    buttonGivens2D.on_clicked(openGivens2D)
    buttonGivens3D.on_clicked(openGivens3D)

    plt.show()



def householder3D():
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    fig.canvas.set_window_title('Householder 3D')
    plt.subplots_adjust(left=0.1, bottom=0.25, right=0.7)
    plotSettings3D()

    def update(val):
        x = [sliderX1.val, sliderX2.val, sliderX3.val]
        k = sliderK.val
        p, v, vp = householder(x, k)

        xx = np.linspace(-3, 3, 5)
        yy = np.linspace(-3, 3, 5)
        xx, yy = np.meshgrid(xx,yy)
        zz = (-v[0]*xx-v[1]*yy)/v[2]

        try:
            ax.lines.remove([line for line in ax.lines if line.get_label()=='x'][0])
            ax.lines.remove([line for line in ax.lines if line.get_label()=='x\''][0])
            ax.lines.remove([line for line in ax.lines if line.get_label()=='v'][0])
            ax.collections.remove([collection for collection in ax.collections if collection.get_label()==r'v$\perp$'][0])
        except IndexError:
            pass

        plotX, = ax.plot([0, x[0]], [0, x[1]], [0, x[2]], zorder=2, color='b', label='x')
        plotP, = ax.plot([0, p[0]], [0, p[1]], [0, p[2]], zorder=2, color='r', label='x\'')
        plotV, = ax.plot([0, v[0]], [0, v[1]], [0, v[2]], zorder=2, color='g', label='v')
        try:
            plotVP, = ax.plot_wireframe(xx, yy, zz, color='m', label=r'v$\perp$')
        except TypeError:
            pass

        ax.legend(loc="upper right")
        plt.draw()

    axesSliderX1 = plt.axes([0.1, 0.2, 0.8, 0.025])
    sliderX1 = Slider(axesSliderX1, r'$x_1$', valmin=-10, valmax=10, valinit=0)
    axesSliderX2 = plt.axes([0.1, 0.15, 0.8, 0.025])
    sliderX2 = Slider(axesSliderX2, r'$x_2$', valmin=-10, valmax=10, valinit=0)
    axesSliderX3 = plt.axes([0.1, 0.1, 0.8, 0.025])
    sliderX3 = Slider(axesSliderX3, r'$x_3$', valmin=-10, valmax=10, valinit=0)
    axesSliderK = plt.axes([0.1, 0.05, 0.8, 0.025])
    sliderK = Slider(axesSliderK, 'k', valmin=0, valmax=2, valinit=0, valstep=1)

    sliderX1.on_changed(update)
    sliderX2.on_changed(update)
    sliderX3.on_changed(update)
    sliderK.on_changed(update)

    axesButtonHouseholder2D = plt.axes([0.7, 0.8, 0.2, 0.05])
    buttonHouseholder2D = Button(axesButtonHouseholder2D, 'Householder 2D')
    axesButtonHouseholder3D = plt.axes([0.7, 0.7, 0.2, 0.05])
    buttonHouseholder3D = Button(axesButtonHouseholder3D, 'Householder 3D')
    axesButtonGivens2D = plt.axes([0.7, 0.6, 0.2, 0.05])
    buttonGivens2D = Button(axesButtonGivens2D, 'Givens 2D')
    axesButtonGivens3D = plt.axes([0.7, 0.5, 0.2, 0.05])
    buttonGivens3D = Button(axesButtonGivens3D, 'Givens 3D')

    def openHouseholder2D(event):
        plt.close()
        householder2D()

    def openHouseholder3D(event):
        plt.close()
        householder3D()

    def openGivens2D(event):
        plt.close()
        givens2D()

    def openGivens3D(event):
        plt.close()
        givens3D()

    buttonHouseholder2D.on_clicked(openHouseholder2D)
    buttonHouseholder3D.on_clicked(openHouseholder3D)
    buttonGivens2D.on_clicked(openGivens2D)
    buttonGivens3D.on_clicked(openGivens3D)

    plt.show()



def givens2D():
    fig, ax = plt.subplots()
    fig.canvas.set_window_title('Givens 2D')
    plt.subplots_adjust(left=0.1, bottom=0.25, right=0.7)
    plotSettings2D()

    def update(val):
        x = [sliderX1.val, sliderX2.val]
        angle = sliderAngle.val
        g = givens(x, 0, 1, angle)

        try:
            ax.lines.remove([line for line in ax.lines if line.get_label()=='x'][0])
            ax.lines.remove([line for line in ax.lines if line.get_label()=='x\''][0])
        except IndexError:
            pass

        plotX, = ax.plot([0, x[0]], [0, x[1]], zorder=2, color='b', label='x')
        plotG, = ax.plot([0, g[0]], [0, g[1]], zorder=2, color='r', label='x\'')

        ax.legend(loc="upper right")
        plt.draw()

    def onClick(event):
        clickX, clickY = event.xdata, event.ydata
        sliderX1.set_val(clickX)
        sliderX2.set_val(clickY)

    fig.canvas.mpl_connect('button_press_event', onClick)

    axesSliderX1 = plt.axes([0.1, 0.15, 0.8, 0.025])
    sliderX1 = Slider(axesSliderX1, r'$x_1$', valmin=-10, valmax=10, valinit=0)
    axesSliderX2 = plt.axes([0.1, 0.1, 0.8, 0.025])
    sliderX2 = Slider(axesSliderX2, r'$x_2$', valmin=-10, valmax=10, valinit=0)
    axesSliderAngle = plt.axes([0.1, 0.05, 0.8, 0.025])
    sliderAngle = Slider(axesSliderAngle, r'$\sphericalangle$', valmin=0, valmax=360, valinit=180)

    sliderX1.on_changed(update)
    sliderX2.on_changed(update)
    sliderAngle.on_changed(update)

    axesButtonHouseholder2D = plt.axes([0.7, 0.8, 0.2, 0.05])
    buttonHouseholder2D = Button(axesButtonHouseholder2D, 'Householder 2D')
    axesButtonHouseholder3D = plt.axes([0.7, 0.7, 0.2, 0.05])
    buttonHouseholder3D = Button(axesButtonHouseholder3D, 'Householder 3D')
    axesButtonGivens2D = plt.axes([0.7, 0.6, 0.2, 0.05])
    buttonGivens2D = Button(axesButtonGivens2D, 'Givens 2D')
    axesButtonGivens3D = plt.axes([0.7, 0.5, 0.2, 0.05])
    buttonGivens3D = Button(axesButtonGivens3D, 'Givens 3D')

    def openHouseholder2D(event):
        plt.close()
        householder2D()

    def openHouseholder3D(event):
        plt.close()
        householder3D()

    def openGivens2D(event):
        plt.close()
        givens2D()

    def openGivens3D(event):
        plt.close()
        givens3D()

    buttonHouseholder2D.on_clicked(openHouseholder2D)
    buttonHouseholder3D.on_clicked(openHouseholder3D)
    buttonGivens2D.on_clicked(openGivens2D)
    buttonGivens3D.on_clicked(openGivens3D)

    plt.show()



def givens3D():
    fig = plt.figure()
    fig.canvas.set_window_title('Givens 3D')
    ax = fig.add_subplot(111, projection='3d')
    plt.subplots_adjust(left=0.1, bottom=0.3, right=0.7)
    plotSettings3D()

    def update(val):
        x = [sliderX1.val, sliderX2.val, sliderX3.val]
        angle = sliderAngle.val
        k = sliderK.val
        if k==2:
            g = givens(x, 0, 1, angle)
        if k==3:
            g = givens(x, 1, 2, angle)

        try:
            ax.lines.remove([line for line in ax.lines if line.get_label()=='x'][0])
            ax.lines.remove([line for line in ax.lines if line.get_label()=='x\''][0])
        except IndexError:
            pass

        plotX, = ax.plot([0, x[0]], [0, x[1]], [0, x[2]], zorder=2, color='b', label='x')
        plotG, = ax.plot([0, g[0]], [0, g[1]], [0, g[2]], zorder=2, color='r', label='x\'')

        ax.legend(loc="upper right")
        plt.draw()

    axesSliderX1 = plt.axes([0.1, 0.25, 0.8, 0.025])
    sliderX1 = Slider(axesSliderX1, r'$x_1$', valmin=-10, valmax=10, valinit=0)
    axesSliderX2 = plt.axes([0.1, 0.2, 0.8, 0.025])
    sliderX2 = Slider(axesSliderX2, r'$x_2$', valmin=-10, valmax=10, valinit=0)
    axesSliderX3 = plt.axes([0.1, 0.15, 0.8, 0.025])
    sliderX3 = Slider(axesSliderX3, r'$x_3$', valmin=-10, valmax=10, valinit=0)
    axesSliderAngle = plt.axes([0.1, 0.1, 0.8, 0.025])
    sliderAngle = Slider(axesSliderAngle, r'$\sphericalangle$', valmin=0, valmax=360, valinit=180)
    axesSliderK = plt.axes([0.1, 0.05, 0.8, 0.025])
    sliderK = Slider(axesSliderK, 'k', valmin=2, valmax=3, valinit=2, valstep=1)

    sliderX1.on_changed(update)
    sliderX2.on_changed(update)
    sliderX3.on_changed(update)
    sliderAngle.on_changed(update)
    sliderK.on_changed(update)

    axesButtonHouseholder2D = plt.axes([0.7, 0.8, 0.2, 0.05])
    buttonHouseholder2D = Button(axesButtonHouseholder2D, 'Householder 2D')
    axesButtonHouseholder3D = plt.axes([0.7, 0.7, 0.2, 0.05])
    buttonHouseholder3D = Button(axesButtonHouseholder3D, 'Householder 3D')
    axesButtonGivens2D = plt.axes([0.7, 0.6, 0.2, 0.05])
    buttonGivens2D = Button(axesButtonGivens2D, 'Givens 2D')
    axesButtonGivens3D = plt.axes([0.7, 0.5, 0.2, 0.05])
    buttonGivens3D = Button(axesButtonGivens3D, 'Givens 3D')

    def openHouseholder2D(event):
        plt.close()
        householder2D()

    def openHouseholder3D(event):
        plt.close()
        householder3D()

    def openGivens2D(event):
        plt.close()
        givens2D()

    def openGivens3D(event):
        plt.close()
        givens3D()

    buttonHouseholder2D.on_clicked(openHouseholder2D)
    buttonHouseholder3D.on_clicked(openHouseholder3D)
    buttonGivens2D.on_clicked(openGivens2D)
    buttonGivens3D.on_clicked(openGivens3D)

    plt.show()



def plotSettings2D():
    plt.gca().set_aspect('equal')

    plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(1))
    plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(1))
    plt.gca().set_axisbelow(True)
    plt.grid()

    plt.axvline(x=0, zorder=1, color='k')
    plt.axhline(y=0, zorder=1, color='k')
    
    plt.xlim(-10, 10)
    plt.ylim(-10, 10)



def plotSettings3D():
    plt.gca().set_xlim3d(-10, 10)
    plt.gca().set_ylim3d(-10, 10)
    plt.gca().set_zlim3d(-10, 10)



if __name__ == "__main__":
    householder2D()
