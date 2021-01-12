import numpy as np
import random as random
import matplotlib.pyplot as plt
from time import time

n=50 #Numero de valores.
It=1000 #El numero de iteraciones. Tienen que ser algun exponente de 1x10^n.

def tiempo_final(tiempo):
	tiempo_calculado=time()
	print('El código tardo %s minutos en ejecutarse.' % ((tiempo_calculado-tiempo)/60))

#La función sirve para generar números aleatorios y darnos nuestra matriz de n valores.
def ar_inicial(n): #Arreglo inicial.
	evol=np.zeros(n)
	for i in range(0,n):
		numeros=random.uniform(0,1) #Aqui se crean los numeros aleatorios entre 0 y 1.
		evol[i]=numeros #Aqui se agregan en nuestra matriz.
	return evol

#Aqui hacemos el paso de observar los cambios
def cambios(n,It):
	evol=[]

	#Llenamos la matriz con la función ar_inicial.
	evol=ar_inicial(n)

	#Aqui es donde se lleva a cabo el paso N.2 que es la ley de evolución.
	entrada=random.randint(1,(n-2))

	#Generamos el valor a de comparación.
	a=(evol[entrada+1]+evol[entrada-1])/2

	#Modificamos que se presenten cambios en nuestros valores.
	if (a>0.5):
		evol[entrada]=(evol[entrada]+a)/evol[entrada]
	return evol

#Generamos una funcion para las sumas de las n iteraciones y la solucion.
def solucion(n,It):
	Intento=np.zeros(n) #Generamos una matriz para inyectar los datos anteriores.
	suma=np.zeros(n) #Generamos una matriz de suma de It dimensiones.
	tiempo=time()
	t1=open("graf_t1.txt","w")
	t2=open("graf_t2.txt","w")
	t3=open("graf_t3.txt","w")
	t4=open("graf_t4.txt","w")
	t5=open("graf_t5.txt","w")

	#Generamos el arreglo de comparación.
	for i in range(0,It+1):
		for j in range(0,n):
			#La llenamos con los valores de los cambios.
			Intento=cambios(n,It)

			#Generamos una matriz de suma para todas las iteraciones.
			suma[j]+=Intento[j]
		#Ahora, ponemos un condicional para graficar a cierta iteracion buscada.
		if (i==(It*0.1)):
			val_graf=promedio(n,suma,It)
			grafica=graficar(n,val_graf,i)
			for i in range(0,n):
				t1.write(str(i+1)); t1.write(" "); t1.write(str(val_graf[i]))
				t1.write("\n")
		if (i==(It*0.25)):
			val_graf=promedio(n,suma,It)
			grafica=graficar(n,val_graf,i)
			for i in range(0,n):
				t2.write(str(i+1)); t2.write(" "); t2.write(str(val_graf[i]))
				t2.write("\n")
		if (i==(It*0.5)):
			val_graf=promedio(n,suma,It)
			grafica=graficar(n,val_graf,i)
			for i in range(0,n):
				t3.write(str(i+1)); t3.write(" "); t3.write(str(val_graf[i]))
				t3.write("\n")
		if (i==(It*0.75)):
			val_graf=promedio(n,suma,It)
			grafica=graficar(n,val_graf,i)
			for i in range(0,n):
				t4.write(str(i+1)); t4.write(" "); t4.write(str(val_graf[i]))
				t4.write("\n")
		if (i==It):
			val_graf=promedio(n,suma,It)
			grafica=graficar(n,val_graf,i)
			for i in range(0,n):
				t5.write(str(i+1)); t5.write(" "); t5.write(str(val_graf[i]))
				t5.write("\n")
	t1.close(); t2.close(); t3.close(); t4.close(); t5.close()
	tardo=tiempo_final(tiempo)

#Generamos una funcion para sacar el valor promedio de cada valor.
def promedio(n,suma,It):
	val_promedio=np.zeros(n) #Creamos nuestra matriz solucion.

	#Hacemos un ciclo para calcular el promedio de cada valor y guardarlo.
	for i in range(0,n):
		val_promedio[i]=suma[i]/It
	#Llamamos la funcion para graficar.
	return val_promedio

#Generamos la funcion que graficara nuestros promedios.
def graficar(n,val_graf,i):
	x=np.zeros(n)
	for j in range(0,n):
		x[j]=j
	fig=plt.figure()
	plt.plot(x,val_graf,'-r')
	plt.title('Evolucion con t=%f' % i)
	plt.xlabel('n')
	plt.ylabel('Evolucion.')
	plt.grid()
	plt.show()

if ( __name__ == '__main__' ):
	final=solucion(n,It)