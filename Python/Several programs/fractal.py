import numpy as np
import matplotlib.pyplot as plt
import random as random
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

#Nos genera dos archivos txt para poder graficar en LaTex y para
#tener las posiciones exactas de nuestro sistema.
def txt(x,y,N):
	t1=open("puntos.txt","w")

	for i in range(0,N-1):
		t1.write(str(x[i])); t1.write(" "); t1.write(str(y[i]))
		t1.write("\n")

	t1.close()

def graficar(puntox,puntoy,xt,yt):
	#colors = np.random.RandomState(1000).rand(10001)
	plt.figure()
	plt.title('Fractal')
	plt.plot(xt,yt,'r')
	plt.scatter(puntox,puntoy,c='black',linewidths=0.001)
	plt.show()

def triangulo():
	xt=np.zeros(4)
	yt=np.zeros(4)

	#Consideremos un triangulo con L=2
	L=2

	a=L/2


	xt[0]=0
	yt[0]=0+a

	xt[1]=xt[0]*np.cos(60)+yt[0]*np.sin(60)
	yt[1]=xt[0]*np.sin(60)+yt[0]*np.cos(60)

	xt[2]=xt[0]*np.cos(60)-yt[0]*np.sin(60)
	yt[2]=-xt[0]*np.sin(60)+yt[0]*np.cos(60)

	xt[3]=xt[0]
	yt[3]=yt[0]

	return xt,yt

def hexagono():
	n=6
	xt=np.zeros(n+1)
	yt=np.zeros(n+1)

	#Consideremos un triangulo con L=2
	L=4

	xt[0]=0
	yt[0]=0
	xt[1]=L;xt[2]=L+L/2;xt[3]=L;xt[4]=0;xt[5]=-L/2
	yt[1]=0;yt[2]=L/2;yt[3]=L;yt[4]=L;yt[5]=L/2
	xt[n]=xt[0]
	yt[n]=yt[0]

	return xt,yt

def cuadrado():
	xt=np.zeros(5)
	yt=np.zeros(5)

	L=2 #Longitud de los aristas del triangulo.
	xt[0]=0
	yt[0]=0
	xt[1]=L; xt[2]=L; xt[3]=0; xt[4]=0
	yt[1]=0; yt[2]=L; yt[3]=L; yt[4]=0

	return xt,yt


def particulas(xt,yt):
	x=xt+random.uniform(-0.25,0.25) #Coord. x para el punto.
	y=yt+random.uniform(-0.25,0.25) #Coord. y para el punto.

	r=np.sqrt((xt)**2+(yt)**2) #Radio 
	rc=np.sqrt((x)**2+(y)**2)
	while (r<rc):
			x=xt+random.uniform(-0.25,0.25) #Coord. x para el punto.
			y=yt+random.uniform(-0.25,0.25) #Coord. y para el punto.
			rc=np.sqrt((x)**2+(y)**2)
	return x,y

def punto_medio(puntox,puntoy,xt,yt):
	y=(puntoy+yt)/2
	x=(puntox+xt)/2
	
	return x,y

def solucion():
	tiempo=time()
	print('Decide la figura a utilizar.')
	print("""
		1 - Triangulo
		2 - Cuadrado
		3 - Hexagono
		""")
	indice=int(input('El indice de la figura escodigo es: '))

	if (indice==1):
		#Generar nuestro triangulo.
		xt,yt=triangulo()
		N=2
	elif (indice==2):
		#Generar nuestro cuadrado.
		xt,yt=cuadrado()
		N=3
	elif (indice==3):
		#Generar nuestro hexagono.
		xt,yt=hexagono()
		N=5

	n=3001 #El numero de particulas a usar.
	puntox=np.zeros(n)
	puntoy=np.zeros(n)

	vertice=random.randint(0,N)
	puntox[0],puntoy[0]=particulas(xt[vertice],yt[vertice])

	for i in range(1,n):
		vertice=random.randint(0,N)
		puntox[i],puntoy[i]=punto_medio(puntox[i-1],puntoy[i-1],xt[vertice],yt[vertice])

	grafica=graficar(puntox,puntoy,xt,yt)
	tiempo_calculado=tiempo_total(tiempo)
	archivo=txt(puntox,puntoy,n)



#Aqui corremos todo el código.
if ( __name__ == '__main__' ):
	solucion=solucion()