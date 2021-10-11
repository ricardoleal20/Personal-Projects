import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from itertools import product, combinations
plt.style.use('seaborn-whitegrid')

datos=pd.read_csv('prueba.txt',header=None, sep=' ')

df = pd.DataFrame({'TimeStep': datos[0], 'Pos. x': datos[1], 'Pos. y': datos[2], 'Pos. z': datos[3]})
unique_times = df['TimeStep'].unique()

box = 40

def latex():
    """
    Función que solamente sirve para dar formato tipo LaTex y poder guardar imagenes en este formato.
    """
    import matplotlib
    matplotlib.use("pgf")
    matplotlib.rcParams.update({
    "pgf.texsystem": "pdflatex",
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
    })

#-------------------------------#
# Plot the initial position     #
#-------------------------------#
# Plot for 2D
fig = plt.figure(figsize=(4,4))
test = df.where(df['TimeStep']==unique_times[-1]).dropna(how='all')
particles = len(test)
plt.scatter(test['Pos. x'],test['Pos. y'], color='goldenrod')
plt.plot([-box/2,box/2,box/2,-box/2,-box/2],[-box/2,-box/2,box/2,box/2,-box/2],color='red', label='Simulation box')
plt.xlim(-box/2-2.5,box/2+2.5) 
plt.ylim(-box/2-2.5,box/2+2.5)
plt.title('Posición inicial: Vista en 2D')
plt.title(f'System at t={0.01*unique_times[-1]}ps with {particles} particles')
plt.legend()
plt.show()

latex()

# Plot for 3D
fig = plt.figure(figsize=(5,7))
ax=fig.add_subplot(111,projection='3d')
ax.view_init(elev=12,azim=120)
ax.scatter(test['Pos. x'],test['Pos. y'],test['Pos. z'], s=45, color='goldenrod')
ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
# make the grid lines transparent
ax.xaxis._axinfo["grid"]['color'] =  (1,1,1,0)
ax.yaxis._axinfo["grid"]['color'] =  (1,1,1,0)
ax.zaxis._axinfo["grid"]['color'] =  (1,1,1,0)
r = [-box/2,box/2]
for s, e in combinations(np.array(list(product(r, r, r))), 2):
    if np.sum(np.abs(s-e)) == r[1]-r[0]:
        ax.plot3D(*zip(s, e), color="red")
ax.set_xlim(-box/2-2.5,box/2+2.5)
ax.set_ylim(-box/2-2.5,box/2+2.5)
ax.set_zlim(-box/2-2.5,box/2+2.5)

ax.set_xlabel('Pos. x')
ax.set_ylabel('Pos. y')
ax.set_zlabel('Pos. z')

#plt.title('Posición inicial: Lennard-Jones')


plt.savefig('initial_pos3.pgf',bbox_inches='tight',pad_inches=0.0)

plt.show()

#--------------------------------------------------#
# Video                                            #
#--------------------------------------------------#
unique_times = df['TimeStep'].unique()

# Function to plot both things
def animate(i):
    global df, unique_times, box
    df_i = df.where(df['TimeStep']==unique_times[i]).dropna(how='all')

    # Clear the plots
    ax.clear()

    # Plot for 3D
    ax.scatter(df_i['Pos. x'],df_i['Pos. y'],df_i['Pos. z'], color='goldenrod')
    r = [-box/2,box/2]
    for s, e in combinations(np.array(list(product(r, r, r))), 2):
        if np.sum(np.abs(s-e)) == r[1]-r[0]:
            ax.plot(*zip(s, e), color="red")

    # Transparent lines
    ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    # make the grid lines transparent
    ax.xaxis._axinfo["grid"]['color'] =  (1,1,1,0)
    ax.yaxis._axinfo["grid"]['color'] =  (1,1,1,0)
    ax.zaxis._axinfo["grid"]['color'] =  (1,1,1,0)

    ax.set_xlim(-box/2-2.5,box/2+2.5)
    ax.set_ylim(-box/2-2.5,box/2+2.5)
    ax.set_zlim(-box/2-2.5,box/2+2.5)

    ax.set_xlabel('Pos. x')
    ax.set_ylabel('Pos. y')
    ax.set_zlabel('Pos. z')

    # Plot for 2D
    ax2.clear()
    ax2.scatter(df_i['Pos. x'],df_i['Pos. y'], color='goldenrod')
    r = [-box/2,box/2]
    ax2.plot([-box/2,box/2,box/2,-box/2,-box/2],[-box/2,-box/2,box/2,box/2,-box/2],color='red')

    ax2.set_xlim(-box/2-2.5,box/2+2.5)
    ax2.set_ylim(-box/2-2.5,box/2+2.5)

    ax2.set_xlabel('Pos. x')
    ax2.set_ylabel('Pos. y')

    fig.suptitle(f'System at time t={round(0.001*unique_times[i],3)}ps', fontsize=16)

def set_figure():
    global box
    fig=plt.figure(figsize=(16,6))

    # For 3D preparation
    ax=fig.add_subplot(121,projection='3d')
    ax.view_init(elev=12,azim=120)

    ax.set_xlim(-box/2-2.5,box/2+2.5)
    ax.set_ylim(-box/2-2.5,box/2+2.5)
    ax.set_zlim(-box/2-2.5,box/2+2.5)

    ax.set_xlabel('Pos. x')
    ax.set_ylabel('Pos. y')
    ax.set_zlabel('Pos. z')

    # For 2D preparation
    ax2=fig.add_subplot(122)

    ax2.set_xlim(-box/2-2.5,box/2+2.5)
    ax2.set_ylim(-box/2-2.5,box/2+2.5)

    ax.set_xlabel('Pos. x')
    ax.set_ylabel('Pos. y')

    return fig,ax,ax2

# First just plot for initial positions
fig,ax,ax2 = set_figure()
animate(0)
plt.show()

# And now, for the animation
fig,ax,ax2 = set_figure()
anim=FuncAnimation(fig,animate,frames=len(unique_times),interval=1, repeat=True)

plt.show()