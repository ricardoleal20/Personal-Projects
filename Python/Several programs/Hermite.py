import numpy as np
from scipy import misc
import matplotlib.pyplot as plt
import seaborn as sns
from time import time
sns.set_style('dark')

#Esta función solo sirve para calcular el tiempo de ejecución del código.
def tiempo_total(tiempo):
	tiempo_calculado=time()
	tiempo_final=(tiempo_calculado-tiempo)
	if (tiempo_final>3600):
		print('El código tardo %s horas en ejecutarse.' % (tiempo_final/3600))
	elif (tiempo_final>60):
		print('El código tardo %s minutos en ejecutarse.' % (tiempo_final/60))
	else:
		print('El código tardo %s segundos en ejecutarse.' % tiempo_final)

#La grafica
def grafica(x,H,n):
	plt.figure()
	plt.title('Polinomio de Hermite normalizado con $n={0:.0f}$.'.format(n))
	plt.plot(x,H,'-r',lw=1)
	plt.xlim(0,50)
	plt.ylim(-0.3,0.4)
	plt.show()

#Archivo txt de escritura.
def txt(x,H,Ix):
	t1=open("hermite.txt","w")

	for i in range(0,Ix):
		t1.write(str(x[i])); t1.write(" "); t1.write(str(H[i]))
		t1.write("\n")

	t1.close()

#Función que calcula el polinomio normalizado de Hermite.
def hermite(x,n):
	Hant=0.0
	H=np.exp(-0.5*(x**2+0.5*np.log(np.pi)))

	if (n>0):
		for m in range(1,n+1):
			Hn=np.sqrt(2/m)*x*H-np.sqrt(1.0-1.0/m)*Hant
			Hant=H
			H=Hn
	return H

def solucion():
	tiempo=time()
	x0=0  #La distancia inicial.
	xf=50 #La distancia final.
	Ix=5001 #La cantidad de pasos a dar.
	dx=(xf-x0)/Ix #El cambio infinitesimal entre un paso y otro.

	x=np.linspace(x0,xf,Ix) #El escrito de x marcado por los intervalos Ix.
	n=700 #Escogemos 50 n para el polinomio de Hermite.

	#Ahora generamos la matriz del sistema Hn(x).
	H=np.zeros(Ix)
	#Ahora, realizamos un ciclo for para los valores de Hn(x).
	for i in range(0,Ix-1):
		H[i]=hermite(x[i],n)

	#Una vez obtenemos los valores, los graficamos.
	graficar=grafica(x,H,n)
	#Esto es para los archivos txt para los datos.
	archivo=txt(x,H,Ix)

	#Entonces, calculamos el tiempo de ejecución del código.
	tiempo_final=tiempo_total(tiempo)

#Esto es para ejecutar el código sin problemas.
if ( __name__ == '__main__' ):
	problema=solucion()