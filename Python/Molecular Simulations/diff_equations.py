import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy import constants, special

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

def euler(Nt,theta_0,v_0,g,l,dt):
    """
    Función que sirve para calcular la solución del pendulo simple con el método numérico de Euler.
    """
    theta=np.zeros(Nt)
    v=np.zeros(Nt)
    theta[0], v[0]=theta_0, v_0
    for i in range(Nt-1):
        #Derivada del tiempo
        v[i+1]=v[i]-dt*(g/l)*np.sin(theta[i])
        #Derivada para la posición
        theta[i+1]=theta[i]+dt*v[i+1]
    return theta, v

def rk(Nt,theta_0,v_0,t,dt,g,l):
    """
    Función que sirve para calcular la solución del pendulo simple con el método de Runge Kutta.
    """
    theta=np.zeros(Nt)
    v=np.zeros(Nt)
    theta[0], v[0]=theta_0, v_0
    for i in range(Nt-1):
        theta_rk, v_rk=rk_4k(theta[i],t[i],v[i],dt,g,l)
        theta[i+1]=theta[i]+theta_rk
        v[i+1]=v[i]+v_rk
    return theta, v

def rk_4k(theta,t,v,dt,g,l):
    """
    Función que ayuda a que funcione el método de Runge Kutta más eficientemente. Aquí se calculan
    las 4 k y l distintas.
    """
    f= lambda t,theta,v,g,l: v
    h= lambda t,theta,v,g,l: -(g/l)*np.sin(theta)
    #K para theta, L para v
    #Para 1
    K1=dt*f(t,theta,v,g,l)
    L1=dt*h(t,theta,v,g,l)
    #Para 2
    K2=dt*f(t+dt/2,theta+K1/2,v+L1/2,g,l)
    L2=dt*h(t+dt/2,theta+K1/2,v+L1/2,g,l)
    #Para 3
    K3=dt*f(t+dt/2,theta+K2/2,v+L2/2,g,l)
    L3=dt*h(t+dt/2,theta+K2/2,v+L2/2,g,l)
    #Para 4
    K4=dt*f(t+dt,theta+K3,v+L3,g,l)
    L4=dt*h(t+dt,theta+K3,v+L3,g,l)
    
    theta_i=(K1/6+K2/3+K3/3+K4/6)
    v_i=(L1/6+L2/3+L3/3+L4/6)

    return theta_i, v_i

def verlet(Nt,theta_0,v_0,t,g,l,dt):
    """
    Función numérica que calcula la solución al pendulo simple utilizando el método de Verlet. 
    """
    theta=np.zeros(Nt)
    v=np.zeros(Nt)
    theta[0], v[0]= theta_0, v_0
    F= lambda theta,g,l: -(g/l)*np.sin(theta)
    #Primer para theta
    theta[1]=theta[0]+(dt**2)*F(theta[0],g,l)
    v[1]=v[0]+(dt/2)*(F(theta[1],g,l)+F(theta[0],g,l))
    for i in range(1,Nt-1):
        theta[i+1]=2*theta[i]-theta[i-1]+(dt**2)*F(theta[i],g,l)
        v[i+1]=v[i]+(dt/2)*(F(theta[i+1],g,l)+F(theta[i],g,l))
    return theta, v

def leap_frog(Nt,theta_0,v_0,t,g,l,dt):
    """
    Función que soluciona el pendulo simple con el método de leap frog.
    """
    theta=np.zeros(Nt)
    v=np.zeros(Nt)
    theta[0], v[0]=theta_0, v_0
    F= lambda theta,g,l: -(g/l)*np.sin(theta)
    #Primer para theta
    theta[1]=theta[0]+(dt**2)*F(theta[0],g,l)
    for i in range(1,Nt-1):
        #Para t-h/2
        v1=(theta[i]-theta[i-1])/dt
        v2=v1+F(theta[i],g,l)*dt

        theta[i+1]=theta[i]+dt*v2
        v[i]=0.5*(v2+v1)
    return theta,v


def sol_an(theta_0,g,l,t,dt):
    """
    Aquí se calcula la solución analítica de theta, donde tambien se calcula la velocidad
    pero esta utilizando el método de Euler.
    """
    f_sen=np.sin(theta_0/2)
    k_ellip=special.ellipk(f_sen**2)
    ellip_function=special.ellipj(k_ellip-np.sqrt(g/l)*t,f_sen**2)[0]
    theta=2*np.arcsin(f_sen*ellip_function)

    #Calcular v
    F= lambda theta,g,l:-(g/l)*np.sin(theta)
    v=np.zeros(len(theta))
    for i in range(len(theta)-1):
        v[i+1]=v[i]+dt*F(theta[i],g,l)
    return theta,v

def plot(t,f1,f2,f3,f4,f5,g1,g2,g3,g4,g5):
    """
    Función para realizar una gráfica del ángulo y la velocidad del sistema.
    """
    fig, axs = plt.subplots(1,2, figsize=(9,4))
    #fig.set_size_inches(w=8, h=2.5)
    
    points=int(len(t)/10)
    #Primer gráfica, posición
    axs[0].plot(t,f1,'--r',label='Analítica')
    axs[0].plot(t,f2,color='blue', marker='o', markevery=points, label='Euler')
    axs[0].plot(t,f3,color='green',marker='s', markevery=points, label='RK 4th')
    axs[0].plot(t,f4,color='purple',marker='H', markevery=points, label='Verlet')
    axs[0].plot(t,f5,color='red',marker='X', markevery=points, label='Leap Frog')
    axs[0].set_ylabel('Angulo')
    axs[0].set_xlabel('Tiempo')
    axs[0].set_title('(a)')
    axs[0].spines['right'].set_visible(False)
    axs[0].spines['top'].set_visible(False)

    #Segunda gráfica, velocidad
    axs[1].plot(t,g1,'--r', label='Analitica')
    axs[1].plot(t,g2,color='blue',marker='o', markevery=points, label='Euler')
    axs[1].plot(t,g3,color='green',marker='s', markevery=points, label='RK 4th')
    axs[1].plot(t,g4,color='purple',marker='H', markevery=points, label='Verlet')
    axs[1].plot(t,g5,color='red',marker='X', markevery=points, label='Leap Frog')
    axs[1].set_ylabel('Velocidad')
    axs[1].set_xlabel('Tiempo')
    axs[1].set_title('(b)')
    axs[1].spines['right'].set_visible(False)
    axs[1].spines['top'].set_visible(False)
    plt.legend()
    #plt.savefig('solution.pgf')
    plt.show()

def plot_error(e1,e2,e3,e4):
    """
    Función para realizar una gráfica del error de las soluciones
    """
    Ngrid=[100*i for i in range(1,11)]
    points=1
    fig, axs=plt.subplots(1, figsize=(4.1,4.1))
    #fig.set_size_inches(w=3, h=2.5)
    plt.plot(Ngrid, e1, color='blue', marker='o', markevery=points, label='Euler')
    plt.plot(Ngrid, e2, color='green', marker='s', markevery=points, label='RK 4th')
    plt.plot(Ngrid, e3, color='blue', marker='H', markevery=points, label='Verlet')
    plt.plot(Ngrid, e1, color='red', marker='X', markevery=points, label='Leap Frog')
    axs.set_yticks([0,0.002, 0.004, 0.006, 0.008, 0.01])
    axs.set_yticklabels(['0%','2e-3%','4e-3%','6e-3%','8e-3%', '1e-2%'])
    plt.xlabel('Numero de grid points')
    plt.ylabel('Error')
    plt.title('Error de la solución')
    plt.ylim(0,0.01)
    plt.legend()
    #plt.savefig('error.pgf')
    plt.show()


def solutions():
    """
    Aquí todo se junta para la solución y gráficas
    """
    #Variables
    g=constants.g
    theta_0=0.99*np.pi
    l=0.5
    v_0=0

    #----------------------#
    # Variables de tiempo  #
    #----------------------#
    tf=10
    Nt=1
    error_euler, error_rk, error_verlet, error_lp= [np.zeros(10) for i in range(4)]
    for i in range(10):
        #----------------------#
        # Zona de recalculo    #
        #----------------------#
        Nt+=100
        dt=tf/(Nt-1)
        t=np.linspace(0,10,Nt)

        #----------------------#
        # Solución analítica   #
        #----------------------#
        theta_an, v_an=sol_an(theta_0,g,l,t,dt)

        #----------------------#
        # Solución numérica    #
        #----------------------#
        theta_euler, v_euler=euler(Nt,theta_0,v_0,g,l,dt)
        theta_rk, v_rk=rk(Nt,theta_0,v_0,t,dt,g,l)
        theta_verlet, v_verlet=verlet(Nt,theta_0,v_0,t,g,l,dt)
        theta_lp, v_lp=leap_frog(Nt,theta_0,v_0,t,g,l,dt)

        #----------------------#
        # Calculo de errores   #
        #----------------------#
        error= lambda t1, t2: (100*(t2[-1]-t1[-1])/t2[-1])
        error_euler[i]=abs(error(theta_euler, theta_an))
        error_rk[i]=abs(error(theta_rk, theta_an))
        error_verlet[i]=abs(error(theta_verlet, theta_an))
        error_lp[i]=abs(error(theta_lp, theta_an))

    plot(t,theta_an,theta_euler,theta_rk,theta_verlet,theta_lp, \
        v_an,v_euler,v_rk,v_verlet,v_lp)

    plot_error(error_euler, error_rk, error_verlet, error_lp)

if __name__=='__main__':
    #latex()
    solutions()