#----------------------------------------------------------------------#
# Este programa obtiene la solución númerica a la ecuación de difusión #
# para comprobar los resultados de una solución analítica. el problema #
# va sobre la difusión de un gas radioactivo dentro de la atmosferca,  #
# proveniente de un suelo contaminado.                                 #
#                                                                      #
#                                                                      #
# Este programa esta realizado para la materia de Métodos Matématicos  #
# de la Física II, como parte del primer laboratorio de entrega.       #
#                                                                      #
# Hecho por Ricardo Leal.                                              #
# emal: ricardo.lealpz@gmail.com                       Fecha: 09/10/20 #
#----------------------------------------------------------------------#

#---------------------------------------#
# Importar las librerias                #
#---------------------------------------#

import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from time import time

def tiempo_total(tiempo):
	tiempo_calculado=time()
	tiempo_final=(tiempo_calculado-tiempo)
	if (tiempo_final>3600):
		print('El código tardo %s horas en ejecutarse.' % (tiempo_final/3600))
		print('\n')
	elif (tiempo_final>60):
		print('El código tardo %s minutos en ejecutarse.' % (tiempo_final/60))
		print('\n')
	else:
		print('El código tardo %s segundos en ejecutarse.' % tiempo_final)
		print('\n')

def CFL(D,dx,dt):
	k=D*(dt/dx**2)
	print("El coeficiente de Courant Friedrichs Lewy (CFL) es",k)
	return k

def CI(x,Ix,t):
	p=np.zeros(Ix)
	for i in range(0,Ix):
		p[i]=0.39
		#p[i]=3*x[i]-2
		#p[i]=3*(x[i]**2)-2
	return p

def BC(xf,k,lam,chi,dx,dt,Ix,t,p):
	p[0]=(1-lam*dt-2*k)*p[0]+2*(k*p[1])+2*(chi*dt)
	#p[0]=p[1]+2*chi*dx
	#p[Ix-1]=0
	p[Ix-1]=xf
	return p

def lder(x,Ix,t):
	derecha=np.zeros(Ix)
	return derecha

def matrizA(Ix,k,dt,lam):
	A=np.zeros((Ix,Ix)) #Comando que genera una matrix de nxn dimensiones.
	A[0,0]=A[Ix-1,Ix-1]=1 #Condiciones de frontera para nuestra matriz.
	
	#Ciclo para generar la matriz de valores A.
	for i in range(1,Ix-1):
		A[i,i-1]=-1*k
		A[i,i]= 1+lam*dt+2*k
		A[i,i+1]=-1*k
	return A

def metodo_implicito(A,lam,chi,dx,dt,Ix,It,x,t,xf,k,p,lder,BC):

	f1=lder(x,Ix,t)

	#Generamos la matrix b para la solución del problema.
	b=p.copy()
	#Ahora le asignamos valores
	for i in range(1,Ix-1):
		b[i]=b[i]+dt*f1[i]

	#Usamos un comando para solucionar la matrix A*p=b
	
	p=np.linalg.solve(A,b)
	p=BC(xf,k,lam,chi,dx,dt,Ix,t,p)
	return p

def init():
	line,=ax.plot(x,pSol[:,0],'r',lw=1)
	title.set_text("Difusion en t={0:.0f}s".format(t[0]))
	return line,title

def interval(i):
	global x,pSol,t
	line.set_data(x, pSol[:,i])
	title.set_text("Difusion en t={0:.0f}".format(t[i-1]))
	return line,title
    
def Graf(x,pSol,t,Ix,It):
    fig, ax = plt.subplots() # setup plot
    ax = plt.axes(xlim=(0,250),ylim=(0,100))
    line,=ax.plot(x,pSol[:,0],'r',lw=1) # setup plot for trajectry
    title=ax.text(0.5,1.05,"Difusion en t={0:.0f}s".format(t[0]),va='center')
    anim=animation.FuncAnimation(fig,interval,init_func=init,fargs=[line],frames=np.arange(0,It,1),interval=20,blit=True)
    plt.show()

def txt(x,t,Ix,It,pSol):
	t1=open("graf_t1.txt","w")
	t2=open("graf_t2.txt","w")
	t3=open("graf_t3.txt","w")
	t4=open("graf_3d.txt","w") #La gráfica en 3D
    #Datos para gráficar en 2d a distintos tiempos.
	for i in range(0,Ix):
		t1.write(str(x[i])); t1.write(" "); t1.write(str(pSol[i,1]))
		t1.write("\n")

		t2.write(str(x[i])); t2.write(" "); t2.write(str(pSol[i,int((It-1)/2)]))
		t2.write("\n")

		t3.write(str(x[i])); t3.write(" "); t3.write(str(pSol[i,int(It-1)]))
		t3.write("\n")

    #Datos para graficar en 3D.
	for j in range(0,It):
		for i in range(0,Ix):
			t4.write(str(x[i])); t4.write(" "); t4.write(str(t[j]))
			t4.write(" "); t4.write(str(pSol[i,j])); t4.write("\n")

	t1.close(); t2.close(); t3.close(); t4.close()


def Solucion( ):
	tiempo=time()
	D=1.0  #Coeficiente de difusión.
	lam=0.005 #Coeficiente lambda.
	chi=0.5 #Coeficiente chi.
	xf=250   #Metros recorridos por el sistema.
	tf=50   #Segundos simulados.
    
	Ix=101
	It=201
	dx=xf/(Ix-1) #El paso finito de la distancia.
	dt=xf/(It-1) #El paso finito del tiempo.
	x=np.linspace(0,xf,Ix)
	t=np.linspace(0,tf,It)

	k=CFL(D,dx,dt) #El coeficiente CFL

    #-----------------#
    #La matriz A.     #
    #-----------------#
    
	A=matrizA(Ix,k,dt,lam)

	pSol=np.zeros((Ix,It))

	for j in range(0,It):
		if (j==0):
			p=CI(x,Ix,t)
			p=BC(xf,k,lam,chi,dx,dt,Ix,t,p)
		else:
			p=metodo_implicito(A,lam,chi,dx,dt,Ix,It,x,t[j-1],xf,k,p,lder,BC)

		for i in range(0,Ix):
			pSol[i,j]=p[i]

	#graficar=Graf(x,pSol,t,Ix,It)
	#archivos=txt(x,t,Ix,It,pSol)
	#tiempo_final=tiempo_total(tiempo)
	
	return x,pSol,t,It



x,pSol,t,It=Solucion()

fig, ax = plt.subplots() # setup plot
#ax = plt.axes(xlim=(0,250),ylim=(-10,100))
line,=ax.plot(0,0,'r',lw=1) # setup plot for trajectry
title=ax.text(0.5,1.05,"Difusion en t={0:.0f}s".format(t[0]),transform=ax.transAxes,va='center')
anim=animation.FuncAnimation(fig,interval,init_func=init,frames=np.arange(0,It),interval=20,blit=True)
plt.show()