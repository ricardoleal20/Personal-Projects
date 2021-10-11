import numpy as np
import pandas as pd
from LJ import Lennard_Jones
import matplotlib.pyplot as plt

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

def LJ(epsilon,sigma,r):
    """
    Compute the potential Lennard-Jones
    """
    P1=(sigma/r)**12
    P2=(sigma/r)**6
    return 4*epsilon*(P1-P2)

epsilon=0.039
sigma=2.934
N_particles = 100
N_simulations = 2500
print_every= 50


box = 40

T0=300
epsilon=0.996
sigma=3.405
m=196.96

dt = 0.01
t = np.arange(0,dt*N_simulations,dt)

x0 = np.zeros((N_particles,3))
v0 = np.ones((N_particles,3))
#m = m*np.ones((N_particles,3))

def lattice_pos(npart,r,box):
    """
    Distribuye homogeneamente npart particulas en una celda
    de 1x1 entre 0 y 1, agregando un r/100% de aleatoriedad. 
    Devuelve un np.array de npart de posiciones x 2 coordenadas

    """

    #Calculo cantidad de celdas por lado
    n = int(np.ceil(np.sqrt(npart)))
    
    #calculo el centro de la celda
    nf = 1.0/float(n)
    
    #Calculo las posiciones de todas las celdas disponibles agregando un r% de randomizacion
    
    celdas = [[i*nf +0.5*nf + r*np.random.uniform(low=-box/2,high=box/2),j*nf + 0.5*nf+ r*np.random.uniform(low=-box/2,high=box/2),k*nf + 0.5*nf+ r*np.random.uniform(low=-box/2,high=box/2)]
              for i in range(n) for j in range(n) for k in range(n)]
    
    #Mezclo las posiciones de las celdas
    np.random.shuffle(celdas)
    
    X = np.array(celdas[0:npart])
    return X


for i in range(N_particles):
    x0[i,:] = [np.random.uniform(low=-box/4,high=box/4),np.random.uniform(low=-box/4,high=box/4),np.random.uniform(low=-box/4,high=box/4)]


def lectura_oro():
    """
    Función de Python que lee un .dat y regresa solamente las coordenadas del sistema.
    """
    data = pd.read_csv('/home/ricardoleal20/Documentos/Github/Personal-Projects/Python/Molecular Simulations/Lennard-Jones/newAu.dat',skiprows=9, header=None, sep=' ')
    df = pd.DataFrame(data)
    df.columns = ['Atomos','ID','Pos. x','Pos. y','Pos. z']
    df.drop(columns={'Atomos','ID'},inplace=True)
    coordenadas = np.zeros(df.shape)
    
    coordenadas[:,0] = df['Pos. x']-76
    coordenadas[:,1] = df['Pos. y']-49
    coordenadas[:,2] = df['Pos. z']-10

    return coordenadas

x0 = lectura_oro()
N_particles = len(x0)
m = m*np.ones((N_particles,3))

Solution = Lennard_Jones(N_simulations, N_particles, dt, x0, T0, m, box, sigma, epsilon, 3, 'prueba.lammpstrj', print_every)

latex()

size = 4

# Initialize time for plot solution
t = np.linspace(0,dt*N_simulations,N_simulations+1)

fig=plt.figure(figsize=(size,size))

# Temperature
plt.plot(t,Solution.Temperature, color='red')
#plt.ylim(Solution.Temperature.max()-1.2,Solution.Temperature.max()+1.2)
plt.title('Temperature ($K$)')
plt.xlabel('Time')
plt.savefig(f't_{N_particles}.pgf')
#plt.show()

# Kinetic Energy
fig=plt.figure(figsize=(size,size))
plt.plot(t,Solution.KEnergy, color='gold')
plt.title('Kinetic Energy ($ev/J$)')
plt.xlabel('Time')
plt.savefig(f'ke_{N_particles}.pgf')
#plt.show()

# Potential energy
fig=plt.figure(figsize=(size,size))
plt.plot(t,Solution.PEnergy, color='purple')
plt.title('Potential Energy ($ev/J$)')
plt.xlabel('Time')
plt.savefig(f'pe_{N_particles}.pgf')
#plt.show()


# Total Energy
fig=plt.figure(figsize=(size,size))
plt.plot(t,Solution.TEnergy, color='green', label='Total Energy')
plt.title('Total Energy ($ev/J$)')
plt.xlabel('Time')
plt.savefig(f'te_{N_particles}.pgf')
#plt.show()

# Pressure
#fig=plt.figure(figsize=(6,6))
#plt.plot(t,Solution.Pressure, color='pink')
#plt.title('Pressure')
#plt.xlabel('Time')
#plt.show()

# g(r)
fig=plt.figure(figsize=(size,size))
plt.plot(Solution.rad_distribuion,Solution.g_function, color='black')
plt.title('$g(r)$')
plt.xlabel('Radius')
plt.ylabel('Average radial distribution')
plt.savefig(f'gr_{N_particles}.pgf')
#plt.show()