#-------------------------------# 
# Libraries                     #
#-------------------------------#

from matplotlib import transforms
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import scipy.constants as cte

#---------------------#
# Variables iniciales #
#---------------------#
N=2000 #Número de simulaciones
Nt=2001 #Número de grid points
tf=512
dt=tf/(Nt-1)
t=np.linspace(0,tf,Nt)

#--------------------#
# Otras variables    #
#--------------------#
lamb=0.5    #Coeficiente de amortiguamiento
sigma=1     #Función de avance aleatorio
kbT=1       #Constante de Boltzman en J/k
m=2.5       #Masa

def IC(Nt):
    """
    Esta función crea los arreglos para v y p con un largo de Nt valores.
    Además, les asigna el valor inicial a ambas funciones.

    Args:
        Nt: Número de grid points para el tiempo.

    Returns:
        v: Matriz para la velocidad.
        P: Matriz para la posición.
    """
    v=np.zeros((Nt,3))
    P=np.zeros((Nt,3))
    v[0,:]=1
    P[0,:]=1
    return v,P

def dW(dt):
    """
    Función que calcula el termino dW y entrega un valor aleatorio
    para generar un proceso meramente estocástico.

    Args:
        dt: Time step finito.

    Returns: 
        dW: Número aleatorio en 3D multiplicado por la desviación estandar.
    """
    global lamb,kbT,sigma
    #return np.random.randn(1,3)*np.sqrt(dt)
    return np.random.randn(1,3)*np.sqrt(2*lamb*kbT*sigma*dt)

def varianza(t,f,id):
    """
    Esta función entrega la varianza analítica y numérica
    de la función f, con el fin de realizar un análisis de convergencia.

    Args:
        t: Array del tiempo
        f: Función a conseguir promedio
        id: Identificados para saber cual función analítica usaremos para el prom
    
    Returns:
        f_var_num: Varianza de la función numérica
        f_var_an: Varianza de la función analitica
    """
    global lamb,m,kbT
    f_var_num=np.zeros(Nt)
    if id=='v':
        f_var_an=(kbT/m)*(1-np.exp(-2*(lamb/m)*t))
    elif id=='p':
        f_var_an=(kbT/(m*(lamb/m)**2))*(2*(lamb/m)*t-3+4*np.exp(-(lamb/m)*t)-2*np.exp(-2*(lamb/m)*t))
    for i in range(Nt):
        f_var_num[i]=np.var(f[i,0,:])
    return f_var_num, f_var_an

def promedio(t,f,id):
    """
    Esta función entrega el promedio analítico y numérico
    de las funciones, con el fin de realizar un análisis de
    convergencia.

    Args:
        t: Array del tiempo
        f: Función a conseguir promedio
        id: Identificados para saber cual función analítica usaremos para el prom
    
    Returns:
        f_prom_num: Promedio de la función numérica
        f_prom_an: Promedio de la función analitica
    """
    global lamb,m
    f_prom_num=np.zeros(Nt)
    if id=='v':
        f_prom_an=f[0,0,0]*np.exp(-(lamb/m)*t)
    elif id=='p':
        f_prom_an=1+f[0,0,0]*(m/lamb)*(1-np.exp(-(lamb/m)*t))
    for i in range(Nt):
        f_prom_num[i]=f[i,0,:].mean()
    return f_prom_num, f_prom_an

def langevin_num(Nt,dt,lamb,m,sigma):
    """
    Función que se encarga de resolver numéricamente la función de langevin.

    Args:
        Nt: Número de grid points en t.
        dt: Time step finito para t.
        lamb: Coeficiente de amortiguamiento.
        m: Masa de las particulas
        sigma: Función de avance aleatorio.

    Returns:
        v: Solución numérica para la velocidad en 3D.
        P: Solución numérica para la posición en 3D.
    """
    v,P=IC(Nt)
    for i in range(Nt-1):
        v[i+1,:]=(1-dt*lamb/m)*v[i,:]+(sigma/m)*dW(dt)
        P[i+1,:]=P[i,:]+dt*v[i,:]
    return v,P

def langevin_num_n(Nt,dt,lamb,m,sigma,N):
    """
    Función que se encarga de resolver numéricamente la función de langevin.

    Esta función realiza un total de N simulaciones (que se pueden ver vistas)
    como un total de N particulas.

    Args:
        Nt: Número de grid points en t.
        dt: Time step finito para t.
        lamb: Coeficiente de amortiguamiento.
        m: Masa de las particulas
        sigma: Función de avance aleatorio.
        N: Número de experimentos/particulas.

    Returns:
        v: Solución numérica para la velocidad en 3D.
        P: Solución numérica para la posición en 3D.
    """
    v_n=np.zeros((Nt,3,N))
    P_n=np.zeros((Nt,3,N))
    print('Se esta realizando la simulación del modelo de Langevin')
    for i in range(N):
        v_n[:,:,i], P_n[:,:,i]=langevin_num(Nt,dt,lamb,m,sigma)
        if i%250==0:
            print('Vamos en la particula {f} de {d}'.format(f=i, d=N))
    print('\n')
    return v_n,P_n

#v,P=langevin_num(Nt,dt,lamb,m,sigma) #Una sola simulación

v_n,P_n=langevin_num_n(Nt,dt,lamb,m,sigma,N) #N simulaciones.

#-------------------------------------# 
# Plot of velocity in 3D position     #
#-------------------------------------#
def plot(t,f,Ylabel,Titulo):
    """
    Función que realiza una gráfica de una sola particula con
    sus tres posiciones como lineas independientes.

    Args:
        t: Array del tiempo.
        f: Función a gráficar, como v o P.
        Ylabel: Un string para colocar como ylabel.
        Titulo: Un string para colocar como titulo.
    
    Returns:
        No hay return, solo una gráfica mostrada en el sistema.
    """
    fig = plt.figure(figsize=(7,7))
    plt.plot(t,f[:,0],label='Position x')
    plt.plot(t,f[:,1],label='Position y')
    plt.plot(t,f[:,2],label='Position z')
    plt.ylim(f.min()-5, f.max()+5)
    plt.xlim(t[0],t[-1])
    plt.ylabel(Ylabel)
    plt.xlabel('Tiempo')
    plt.legend()
    plt.title(Titulo)
    plt.show()
    return print('Se genero una gráfica en 2D\n')

def plot_n(t,f,Ylabel,Titulo):
    """
    Función que realiza tres gráficas acopladas para cada una
    de las dimensiones de las particulas.

    Args:
        t: Array del tiempo.
        f: Función a gráficar, como v_n o P_n.
        Ylabel: Un string para colocar como ylabel.
        Titulo: Un string para colocar como titulo.
    
    Returns:
        No hay return, solo una gráfica mostrada en el sistema.
    """
    fig,axs=plt.subplots(3,figsize=(10,10), sharex=True)
    fig.suptitle(Titulo, fontsize=18)
    #Posicion en x
    axs[0].set_title('Position x')
    axs[0].plot(t,f[:,0,:])
    axs[0].set_ylabel(Ylabel)
    axs[0].set_ylim(f[:,0,:].min()-5,f[:,0,:].max()+5)
    axs[0].spines['bottom'].set_visible(False)
    axs[0].spines['right'].set_visible(False)
    axs[0].spines['top'].set_visible(False)
    axs[0].grid(True)
    #Posicion en y
    axs[1].set_title('Position y')
    axs[1].plot(t,f[:,1,:])
    axs[1].set_ylabel(Ylabel)
    axs[1].set_ylim(f[:,1,:].min()-5,f[:,1,:].max()+5)
    axs[1].spines['bottom'].set_visible(False)
    axs[1].spines['right'].set_visible(False)
    axs[1].spines['top'].set_visible(False)
    axs[1].grid(True)
    #Posicion en z
    axs[2].set_title('Position z')
    axs[2].plot(t,f[:,2,:])
    axs[2].set_xlim(t[0],t[-1])
    axs[2].set_ylim(f[:,2,:].min()-5,f[:,2,:].max()+5)
    axs[2].set_xlabel('Tiempo')
    axs[2].set_ylabel(Ylabel)
    axs[2].spines['right'].set_visible(False)
    axs[2].spines['top'].set_visible(False)
    axs[2].grid(True)
    #return print('Se genero una gráfica en 2D\n')

def plot_prom(t,f,id,Ylabel):
    f_prom_num, f_prom_an=promedio(t,f,id=id)
    fig=plt.figure(figsize=(7,7))
    plt.plot(t,f_prom_an, '--r', label='Promedio analítico')
    plt.plot(t,f_prom_num, color='teal', label='Promedio numérico')
    plt.title('Promedio del sistema en 1D')
    plt.xlabel('Tiempo')
    plt.ylabel('Promedio de la '+Ylabel)
    plt.legend()

def plot_var(t,f,id,Ylabel):
    f_var_num, f_var_an=varianza(t,f,id=id)
    fig=plt.figure(figsize=(7,7))
    plt.plot(t,f_var_an, '--r', label='Varianza analítica')
    plt.plot(t,f_var_num, color='teal', label='Varianza numérica')
    plt.title('Varianza del sistema en 1D')
    plt.xlabel('Tiempo')
    plt.ylabel('Varianza de la '+Ylabel)
    plt.legend()
    plt.show()


#plot(t,v,Ylabel='Velocidad (m/s)',Titulo='Velocidad del sistema')
#plot(t,P,Ylabel='Posición',Titulo='Posición de las particulas')

#Para la velocidad
print('Se estan realizando gráficas de la velocidad.')
plot_n(t,v_n,'Velocidad (m/s)','Velocidad del sistema')
plot_prom(t,v_n,id='v',Ylabel='velocidad')
plot_var(t,v_n,id='v',Ylabel='velocidad')

#Para la posición
print('Se estan realizando gráficas de la posición.')
plot_n(t,P_n,'Coordenada','Posición de las particulas')
plot_prom(t,P_n,id='p',Ylabel='posición')
plot_var(t,P_n,id='p',Ylabel='posición')


#------------------------------------------------------#
# 3D Plot animation                                    #
#------------------------------------------------------#

fig = plt.figure(figsize=(10,10))
ax=Axes3D(fig)
ax.view_init(elev=12,azim=120)

ax.set_xlim(-50,50)
ax.set_ylim(-50,50)
ax.set_zlim(-50,50)

ax.set_xlabel('Pos. x')
ax.set_ylabel('Pos. y')
ax.set_zlabel('Pos. z')
plt.title('Sistema al tiempo t={0:.2f}s'.format(t[0]))

p_line, = ax.plot([],[],[], color='red', ms=8, alpha=0.5)

def animate(i,p_line,P_n,v_n,t):
    ax.clear()
    ax.scatter(P_n[i,0,:],P_n[i,1,:],P_n[i,2,:], color='teal')
    ax.set_xlim(-20,20)
    ax.set_ylim(-20,20)
    ax.set_zlim(-20,20)
    ax.set_xlabel('Pos. x')
    ax.set_ylabel('Pos. y')
    ax.set_zlabel('Pos. z')
    ax.text(-180,0,250,'Sistema al tiempo t={0:.2f}s'.format(t[i]),transform=ax.transAxes,va='center')

    #p_line.set_data(P[i,0], P[i,1])
    #p_line.set_3d_properties(P[i,2])
     

print('Se esta generando una animación. Porfavor espere.')

#anim=FuncAnimation(fig,animate,frames=[x for x in range(0,Nt,int(Nt/Nt))],fargs=(p_line,P_n,v_n,t),interval=200, repeat=False)
#anim.save('langevin.mp4',fps=20)
plt.show()