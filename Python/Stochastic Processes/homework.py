import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')

def plot(y,yan,t):
    plt.figure()
    #plt.title('$\frac{dy(t)}{dt}=-y(t)$ with $y(0)=1$')
    plt.xlabel('y(t) values.')
    plt.ylabel('t values.')
    plt.plot(t,y,'--r',lw=3,label='Numerical solution.')
    plt.plot(t,yan,'--b',lw=1,label='Analytical solution.')
    plt.plot(t,y/yan,lw=1)#,label='Ratio $\frac{y}{y_{an}}$')
    plt.show()

def runge(IC,t,It):
    y=np.zeros(It) #This is for create the little matrix for the values of y.
    y[0]=IC
    
    for i in range(0,It-1):
        
        k1=-y[i]
        k2=-0.5*dt*y[i]
        
        y[i+1]=y[i]-0.5*dt*(k1+k2)
    return y

dt  = 0.01 #This is the infinitisemal changes in the time.
t0  = 0    #This is the initial time of simulation.
tf  = 10   #This is the final time of simulation.
It  = int(((tf-t0)/dt)) #This is the total of steps made with dt.

t   = np.linspace(t0,tf,It) #Get the same t values that we are going to get with the dt.
yan =np.exp(-t) #This is the analytical solution.

IC  =1.0  #This is the initial condition of the system. 

y   =runge(IC,t,It) #It call the function of Runge Kutta to get the numerical values of y.
graf=plot(y,yan,t)  #This will graph the solutions.