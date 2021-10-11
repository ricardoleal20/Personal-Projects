import numpy as np
from rdfpy import rdf
from scipy.constants.constants import Avogadro, Boltzmann, eV
from dump import writeOutput as dump_l
from dump import writeOutput_python as dump_p
from time import time

class Lennard_Jones:
    def __init__(self,
                n_simulations, 
                N_particles,
                dt,
                x0,
                T0,
                m,
                box,
                sigma,
                epsilon,
                dim: int,
                filename: str,
                print_every: int):
        """
        A ver que pones
        """
        # Initialize the time
        initial_time = time()
        

        #Solve the system
        self.SimulateSystem(n_simulations,N_particles,dt,x0,T0,m,box, sigma, epsilon, dim, filename, print_every)

        # Print the total time of simulation
        self.total_time(initial_time)

    #Put all together
    def SimulateSystem(self,
                       n_simulations, 
                       N_particles,
                       dt,
                       x0,
                       T0,
                       m,
                       box,
                       sigma,
                       epsilon,
                       dim: int,
                       filename: str,
                       print_every: int):
        """
        Por ahora no pongas nada
        """

        n_simulations+=1

        # Initialize some variables
        dim = len(x0[0,:]) # Dimension of the system to simulate
        v0 = self.init_velocity(T0,m,N_particles,dim) # Initial velocity
        #v0 = np.random.randn(N_particles,dim)

        #----------------------------------------#
        # Rescale some variables                 #
        #----------------------------------------#
        rho = 0.3

        # Open files to grab text 
        file = open('prueba.txt','w')

        # Temperature,pressure and energy
        E = np.zeros((n_simulations,2))
        T = np.zeros(n_simulations)
        P = np.zeros(n_simulations)

        r_cut = abs(box)/2 # Rescaled units of the box
        F, E[0,0]=self.Force(N_particles,x0,r_cut,box,epsilon,sigma) # Initial Force

        # Initial values for E
        T[0] = T0
        E[0,1] = 0.5*np.sum(np.power(v0,2))
        P[0] = rho*T[0]

        print('Step:',0,'|Temperature:',T[0],'|Pot. Energy:',E[0,0],'|Kin. Energy:',E[0,1],'|Pressure:',P[0])
        dump_p(file,N_particles,0,box,position=x0,v=v0)

        # Do a for cicle to performs the entire set of simulations
        for step in range(1,n_simulations):
            # Create the arrays for x and v with values in it
            x,v= x0,v0

            # Compute the forces
            Fn,E[step,0]=self.Force(N_particles,x,r_cut,box,epsilon,sigma)

            # Get the new values for x and v
            x,v=self.SolveMotion(x,v,dt,m,F,Fn)

            # Calculate the Kinetic energy of the system
            E[step,1] = 0.5*np.sum(np.power(v,2))

            # Compute the temperature of the system
            T[step] = E[step,1]/(2)

            # Compute the pressure of the box
            P[step] = rho*T[step]+P[step-1]/(dim*box**dim)

            # Check the position of the particle
            x = self.Check_Periodicity(x,box,N_particles)

            # Print the data if it's need it
            if not (step)%print_every:
                print('Step:',step,'|Temperature:',round(T[step],3),'|Pot. Energy:',round(E[step,0],3),'|Kin. Energy:',round(E[step,1],3),'|Pressure:',round(P[step],3))
                #dump_l(filename,N_particles,step+1,box,pos=x,v=v)
                dump_p(file,N_particles,step,box,position=x,v=v)

            if step==1:
                dif = T[step]-T[0]
                T[0]=T[step]-dif/100

            # Set x0 and v0 as the new x & v. Do it also with F
            x0,v0,F= x,v,Fn # Repeat the cicle until step=n_simulations
        
        # Make accesible the others Variables
        self.Temperature=T
        self.Pressure=P
        self.Energy=E # To get bot energy
        self.PEnergy=E[:,0]
        self.KEnergy=E[:,1]
        self.TEnergy=E[:,0]+E[:,1]
        self.g_function, self.rad_distribuion=self.g(x)

        file.close()

    #Forces
    def Force(self,npart,pos,rcut,box,epsilon,sigma):
        """
        Compute the forces of all the particles using a Lennard-Jones potential. The distances have been reduces by sigma
        and use a rcut radius to cut the potential.
        """     
        # Initialize the values for F and Potential energy
        F = np.zeros((npart,len(pos[0,:])))

        # xd
        lenght_box = box

        Epot = 0.0

        m = 9
        n = 6

        k = m/(m-n)*(m/n)**(n/(m-n))
    
        # Get the cutoff energy
        rci6 = 1.0/rcut**6
        rci12= rci6**2
        Ecut = 4*(rci12 -rci6)

    
        # Get the force between the particles
        for i in range(npart-1):
            for j in range(i+1,npart):

                # Get the difference between the positions
                dr = pos[i,:] - pos[j,:]
                #dr = dr - lenght_box*np.rint(dr/lenght_box)
                
                r_square = np.sum(np.power(dr,2))

                if np.sqrt(r_square) < 1:
                    continue
                elif r_square < rcut**2:

                    # Get the force of the system
                    r = np.sqrt(r_square)
                    #r1=1/r_square
                    #r6=r1**5

                    #Force = 48*r6*r1*(r6-0.5)
                    Force = k*1*(m*(1**m/r**(m+1))-n*(1**n/r**(n+1)))
                
                    F[i,:] = F[i,:] + Force*dr[:]
                    F[j,:] = F[j,:] - Force*dr[:]

                    # Now, get the potential Energy
                    #Epot+=4*r6*(r6-1)
                    Epot+=k*1*((1/r)**m-(1/r)**n)


                
        return [F,Epot] # Force in reduced units and energy in kj/mol

    def LJ(self,epsilon,sigma,r):
        """
        Compute the potential Lennard-Jones
        """
        P1=np.power(sigma/r,12)
        P2=np.power(sigma/r,6)

        xd = 4 * epsilon * np.power(sigma/r, 12)/r - np.power(sigma/r, 6)

        return 4*epsilon*P1/r-P2

    def SolveMotion(self,x,v,dt,m,F,Fn):
        """
        Solve the motion of the particles using Verlet scheme
        """

        # Calculate the new position
        x_n=x+v*dt+0.5*((dt**2)/m)*F

        # Calculate the new velocity
        v_n=v+0.5*(dt/m)*(Fn+F)

        return x_n,v_n

    def Check_Periodicity(self,x,box,n_part):
        """
        Check the position of the particle and move it to another place if the particle
        if set beyond the box of simulation.
        """
        #For 1D
        for i in range(len(x[0,:])):
            mask1 = np.where(x[:,i] > box/2)
            mask2 = np.where(x[:,i] < -box/2)

            x[mask1,i] = x[mask1,i] - box
            x[mask2,i] = x[mask2,i] + box
            

        return x

    def init_velocity(self,T,m,N_particles,dim):
        """
        Initialize the velocity of a system
        """
        v = np.zeros((N_particles,dim)) # Create the particles

        # Create the initial array of the velocities
        theta = 2*np.pi*np.random.rand(N_particles)

        # Magnitue of Velocity
        v_mag = np.sqrt(dim*T/N_particles)

        # Now, assign the values of velocity
        v[:,0] = np.cos(theta)*v_mag
        v[:,1] = np.sin(theta)*v_mag
        v[:,2] = np.cos(theta)*v_mag

        return v

    def g(self,pos):
        """
        Ahorita lo comentas
        """
        g_r, radii = rdf(pos, dr=0.1)
        return g_r, radii

    def total_time(self,tiempo):
        tiempo_calculado=time()
        tiempo_final=(tiempo_calculado-tiempo)
        if (tiempo_final>3600):
            print(f'La simulación tardo {round(tiempo_final/3600,2)} horas en ejecutarse.')
        elif (tiempo_final>60):
            print(f'La simulación tardo {round(tiempo_final/60,2)} minutos en ejecutarse.')
        else:
            print(f'La simulación tardo {round(tiempo_final,2)} segundos en ejecutarse.')


#-------------------------------------------------------------#
# Test of the code just to see if works                       #
#-------------------------------------------------------------#
