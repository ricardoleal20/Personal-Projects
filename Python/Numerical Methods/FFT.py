import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.animation import FuncAnimation
from scipy.fft import fft, ifft, fftfreq
from time import time

def tiempo_total(tiempo):
	tiempo_calculado=time()
	tiempo_final=(tiempo_calculado-tiempo)
	if (tiempo_final>3600):
		print('El código tardo {0:.2f} horas en ejecutarse.'.format(tiempo_final/3600))
		print('\n')
	elif (tiempo_final>60):
		print('El código tardo {0:.2f} minutos en ejecutarse.'.format(tiempo_final/60))
		print('\n')
	else:
		print('El código tardo {0:.2f} segundos en ejecutarse.'.format(tiempo_final))
		print('\n')

def CFL(alpha,dt,dx):
    k=alpha*dt/dx**2
    print('El valor del criterio CFL es k={0:.4f}'.format(k))
    return k

def IC(Nx,Nt,x):
    """
    Function that creates the matrix solution and put the initial condition of the system.

    Args:
        Nx: Number of grid points for x
        Nt: Number of grid points for t
        x: Array of the position
    
    Returns:
        T: Numerical solution of the heat equation
    """
    T=np.zeros((Nx,Nt))
    #T[:,0]=6*np.sin(np.pi*x/x[-1])
    T[:,0]=12*np.sin(9*np.pi*x/x[-1])-7*np.sin(4*np.pi*x/x[-1])
    return T

def dW(dt,n):
    return np.random.random(size=n)*np.sqrt(dt)

def derivative_fft(f,N,dx,n):
    """
    This function calculates the numerical derivative of n-order using the FFT method. 

    Args:
        f: Function to calculate the derivative
        N: Number of gridpoints
        dx: Finite step
        n: Order of the derivative

    Returns:
        dfdx: Numerical and exact derivative
     """
    fHat=fft(f)        #First, create the Fourier function f
    k=2*np.pi*fftfreq(N,d=dx) #Now, create the spatial wavelenght
    dfHat=fHat*(1j*k)**n      #Now, calculate the fourier derivative
    return ifft(dfHat).real #Use the inverse Fourier transform to get df

def sol_analitica(x,t,alpha,Nx,Nt):
    """
    Function to solve the heat equation using analitical methods.

    Args:
        x: Array of the position
        t: Array of the time
        alpha: Diffusion constant
        Nx: Number of grid points for x
        Nt: Number of grid points for t
    
    Returns:
        T: Numerical solution of the heat equation
    """
    T=np.zeros((Nx,Nt))
    for i in range(Nt):
        #T[:,i]=6*np.sin(np.pi*x/x[-1])*np.exp(-alpha*t[i]*(np.pi/x[-1])**2)
        T[:,i]=12*np.sin(9*np.pi*x/x[-1])*np.exp(-alpha*t[i]*(9*np.pi/x[-1])**2)-7*np.sin(4*np.pi*x/x[-1])*np.exp(-alpha*t[i]*(4*np.pi/x[-1])**2)
    return T

def sol_diff(Nx,Nt,x,k):
    """
    Function that use the finite difference method to solve the heat equation. I use a 3-points aproximation
    for the second derivative, and for the time derivative I use forward Euler.

    Args:
        Nx: Number of grid points for x
        Nt: Number of grid points for t
        x: Array of the position
        k: CFL variable

    Returns:
        T: Numerical solution of the heat equation
    """
    T=IC(Nx,Nt,x)
    for j in range(0,Nt-1):
        dTdx=T[2:,j]-2*T[1:-1,j]+T[:-2,j]
        T[1:-1,j+1]=T[1:-1,j]+k*dTdx
    return T

def stoc_sol_diff(Nx,Nt,x,k,dt):
    """
    Function that use the finite difference method to solve the heat equation. I use a 3-points aproximation
    for the second derivative, and for the time derivative I use forward Euler.

    Args:
        Nx: Number of grid points for x
        Nt: Number of grid points for t
        x: Array of the position
        k: CFL variable

    Returns:
        T: Numerical solution of the heat equation
    """
    T=IC(Nx,Nt,x)
    for j in range(0,Nt-1):
        sigma=np.random.uniform(low=-10,high=10)
        dTdx=T[2:,j]-2*T[1:-1,j]+T[:-2,j]
        T[1:-1,j+1]=T[1:-1,j]+k*dTdx+sigma*dW(dt, n=T[1:-1,j].size)
    return T

def sol_fft(Nx,Nt,x,alpha,dx,dt):
    """
    Function that use the FFT method to solve the Heat Equation. For the time derivative, it use
    forward Euler to solve it. Apply a boundary conditions of T[0,t]=T[L,t]=0

    Args:
        Nx: Number of grid points for x
        Nt: Number of grid points for t
        x: Array for the position
        alpha: Diffusion constant
        dx: Finite position-step
        dt: Finite time-step

    Returns:
        T: Numerical solution of the heat equation
    """
    T=IC(Nx,Nt,x)
    for j in range(Nt-1):
        T[:,j+1]=T[:,j]+dt*alpha*derivative_fft(T[:,j],Nx,dx,2)
        T[0,j+1]=0
        T[-1,j+1]=0
    return T

def stoc_sol_fft(Nx,Nt,x,alpha,dx,dt):
    """
    Function that use the FFT method to solve the Heat Equation. For the time derivative, it use
    forward Euler to solve it. Apply a boundary conditions of T[0,t]=T[L,t]=0

    Args:
        Nx: Number of grid points for x
        Nt: Number of grid points for t
        x: Array for the position
        alpha: Diffusion constant
        dx: Finite position-step
        dt: Finite time-step

    Returns:
        T: Numerical solution of the heat equation
    """
    T=IC(Nx,Nt,x)
    for j in range(Nt-1):
        sigma=np.random.uniform(low=-10,high=10)
        T[:,j+1]=T[:,j]+dt*alpha*derivative_fft(T[:,j],Nx,dx,2)+sigma*dW(dt,n=T[:,j].size)
        T[0,j+1]=0
        T[-1,j+1]=0
    return T

def plot(x,T,Nt):
    """
    Function that plot the solution for different times.

    Args:
        x: Array of the position
        T: Solution matrix
        Nt: Number of grid points for the time

    Retuns:
        Pop-up the plot
    """
    fig, axs=plt.subplots(1,figsize=(7,7))
    plt.plot(x,T[:,0], label='$t=0$s')
    plt.plot(x,T[:,int((Nt-1)/3)],label='$t=\\frac{tf}{3}$')
    plt.plot(x,T[:,int(2*(Nt-1)/3)],label='$t=\\frac{2tf}{3}$')
    plt.plot(x,T[:,-1], label='$t=tf$')
    plt.xlabel('Position $(x)$')
    plt.ylabel('Temperature $(K)$')
    plt.title('Solution of the heat equation using FFT')
    axs.spines['top'].set_visible(False)
    axs.spines['right'].set_visible(False)
    plt.legend()
    plt.show()

def plot_animation(x,t,T_fft,T_dm,T_an,Nx,Nt):
    """
    Function that creates a gif of the solution of the system. It compares the analitical, finite and pseudo-spectral solution.

    Args:
        x: Array of the position
        t: Array of the time
        T_fft: Solution using the FFT method
        T_dm: Solution using the FDM method
        T_an: Analitical solution
        Nx: Number of grid points for the position
        Nt: Number of grid points for the time

    Retuns:
        Show the animate plot
    """
    fig, axs=plt.subplots(1,figsize=(7,7))
    plt.title('Sistema al tiempo t={0:.2f}s'.format(t[0]))
    line1,=plt.plot([],[],'--r',label='Analytic')
    line2,=plt.plot([],[],color='teal', alpha=0.7,markevery=int(Nx/5),marker='o',label='FDM 3p')
    line3,=plt.plot([],[],color='green', alpha=0.7,markevery=int(Nx/5),marker='.',label='FFT')
    axs.spines['top'].set_visible(False)
    axs.spines['right'].set_visible(False)
    plt.xlim(x[0],x[-1])
    plt.ylim(T_an.min()-1,T_an.max()+1)
    plt.xlabel('Position $(x)$')
    plt.ylabel('Temperature $(K)$')
    plt.legend()

    times=[i for i in range(0,Nt,int(Nt/120))]
    times.append(Nt-1)

    anim=FuncAnimation(fig,animate,frames=times,fargs=(line1,line2,line3,x,t,T_fft,T_dm,T_an),interval=1,repeat=True)
    plt.show()

def animate(i,line1,line2,line3,x,t,T_fft,T_dm,T_an):
    """
    Function that work with FuncAnimation to create an animation of the solution.

    Args:
        i: Frame
        line1: First line to plot
        line2: Second line to plot
        line3: Third line to plot
        x: Array of the position
        t: Array of the time
        T_fft: Solution using the FFT method
        T_dm: Solution using the FDM method
        T_an: Analitical solution

    Returns:
        line1, line2, line3 : Block of the animate plot    
    """
    line1.set_data(x,T_an[:,i])
    line2.set_data(x,T_dm[:,i])
    line3.set_data(x,T_fft[:,i])
    plt.title('Sistema al tiempo t={0:.2f}s'.format(t[i]))
    return line1, line2, line3,

def heat_equation(stochastic):
    #-------------------------------------#
    # Variables espacio                   #
    #-------------------------------------#
    alpha=0.5

    Nx=101
    xf=50
    dx=xf/(Nx-1)
    x=np.linspace(0,xf,Nx)

    #-------------------------------------#
    # Variables tiempo                    #
    #-------------------------------------#
    tf=50
    Nt=1001
    dt=tf/(Nt-1)

    t=np.linspace(0,tf,Nt)
    tiempo=time()

    #-------------------------------------#
    # Checar CFL condition                #
    #-------------------------------------#
    k=CFL(alpha,dt,dx)

    #-------------------------------------#
    # Solución de la ecuación             #
    #-------------------------------------#
    T_an=sol_analitica(x,t,alpha,Nx,Nt)

    print('Se esta realizando la simulación.')
    if stochastic=='yes':
        N=int(2e3)
        print('Es una simulación estocástica con {0:.0f} experimentos'.format(N))
        Tn_dm=np.zeros((Nx,Nt))
        Tn_fft=np.zeros((Nx,Nt))
        for i in range(N):
            if i%100==0:
                print('Vamos en el frame {0:.0f}'.format(i))
            Tn_dm[:,:]+=(stoc_sol_diff(Nx,Nt,x,k,dt))
            Tn_fft[:,:]+=(stoc_sol_fft(Nx,Nt,x,alpha,dx,dt))
        T_dm=Tn_dm/N
        T_fft=Tn_fft/N
    else:
        print('Es una simulación determinista')
        T_dm=stoc_sol_diff(Nx,Nt,x,k,d)
        T_fft=stoc_sol_fft(Nx,Nt,x,alpha,dx,dt)


    tiempo_total(tiempo)



    #-------------------------------------#
    # Gráficar                            #
    #-------------------------------------#

    print('Se esta gráficando.')
    plot(x,T_fft,Nt)
    print('Se esta creando una animación.')
    plot_animation(x,t,T_fft,T_dm,T_an,Nx,Nt)


if __name__=='__main__':
    heat_equation(stochastic='yes')