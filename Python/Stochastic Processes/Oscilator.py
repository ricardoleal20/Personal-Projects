import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
plt.style.use('ggplot')


dim= 2  #The dimension of the system.
N= 1000 #The number of steps
R=np.zeros(dim) #The position of the particle
V=np.zeros(dim) #The velocity of the particle
Rs=np.zeros([dim,N]) #The position of the particle in all the steps
Vs=np.zeros([dim,N]) #The velocity of the particle in all the steps
Et=np.zeros(N) #The total energy of the system
time=np.zeros(N) #The total time of the system

#It use to initizalize animation
def init():
	particles.set_data([], [])
	line.set_data([], [])
	title.set_text(r'')
	return particles,line,title

#The animation using Euler method
def animate(i):
	global R,V,F,Rs,Vs,time,Et
	R, V =R+V*dt, V*(1-zeta/m*dt)-k/m*dt*R #The Euler equations
	Rs[0:dim,i]=R
	Vs[0:dim,i]=V
	time[i]=i*dt
	Et[i]=0.5*m*np.linalg.norm(V)**2+0.5*k*np.linalg.norm(R)**2
	particles.set_data(R[0], R[1])
	line.set_data(Rs[0,0:i], Rs[1,0:i])
	title.set_text(r"$t={0:.02f},E_T={1:.3f}$".format(i*dt,Et[i]))
	return particles,line,title

# System parameters
# particle mass, spring & friction constants
m, k, zeta = 5.0, 1.0, 0.25
# Initial condition
R[0], R[1] = 1., 1. # Rx(0), Ry(0)
V[0], V[1] = 1., 0. # Vx(0), Vy(0)
dt   = 0.1*np.sqrt(k/m) # set \Delta t
box  = 5 # set size of draw area
# set up the figure, axis, and plot element for animatation
fig, ax = plt.subplots(figsize=(7.5,7.5)) # setup plot
ax = plt.axes(xlim=(-box/2,box/2),ylim=(-box/2,box/2)) # draw range
particles, = ax.plot([],[],'ko', ms=10) # setup plot for particle 
line,=ax.plot([],[],lw=1) # setup plot for trajectry
title=ax.text(0.5,1.05,r'',transform=ax.transAxes,va='center') # title
anim=animation.FuncAnimation(fig,animate,init_func=init,
     frames=N,interval=5,blit=True,repeat=False) # draw animation
anim.save('movie.mp4',fps=20,dpi=400)