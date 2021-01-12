import numpy as np
import scipy as sp
import math as math
import scipy.integrate as integrate
from scipy import special
import matplotlib.pyplot as plt
from time import time
plt.style.use('ggplot')


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

def grafica(t,u,N):
	x=np.zeros(N)
	for i in range(1,N):
		x[i]=i
	figura=plt.figure()
	plt.title('Nuestra onda en t={0:.0f}'.format(t))
	plt.ylabel('$u(r,{0:.0f})$'.format(t))
	plt.xlabel('r')
	plt.plot(x,u,'-r')
	#plt.grid()
	plt.show()

def txt(t,u,N,j):
	t1=open("grafica_t{0:.0f}.txt".format(j),"w")

	for i in range(0,N):
		t1.write(str(i)); t1.write(" "); t1.write(str(u[i]))
		t1.write("\n")

	t1.close()

def valores_lam():
	lam=np.zeros(6)

	for i in range(1,6):
		lam[i]=5*i

	return lam

def factorial(n): 
    factor = 1
    i = 1
    while i <= n:
        factor = factor * i
        i = i + 1
    return factor

def c(i,n,alp,lam):
	#La funcion de Bessel para Cn
  	J1=special.jv(1,alp)

  	#El argumento para la funcion sinh.
  	argumento=lam*5

  	#Los argumentos a integrar. El primer termino del lambda es la función.
  	x= lambda i:(5*i-1)*special.jv(0,alp*i)*i

  	#Es la fracción para cn.
  	frac=1/(2*(J1**2)*(np.sinh(argumento)))
  	#La integral de cn.
  	inte,error=integrate.quad(x,0,2)
  	#El final de cn
  	cn=frac*inte

  	return cn

def a(i,n,alp,lam):
	#La funcion de Bessel para Cn
  	J1=special.jv(1,alp)

  	#El argumento para la funcion sinh.
  	argumento=lam*5

  	#Los argumentos a integrar.El primer termino del lambda es la función.
  	x= lambda i:(3*i+2)*special.jv(0,alp*i)*i

  	#Es la fracción para an.
  	frac=1/(2*(J1**2)*(np.sinh(argumento)))
  	#La integral de an.
  	inte,error=integrate.quad(x,0,2)
  	#El final de an
  	an=frac*inte

  	return an

#Funcion factorial para la solución numérica del problema 5.
def funcion_factorial(n):
    #La parte de arriba de la fracción.
	arriba=((-1)**n)*2*factorial(n)
	#La parte de abajo de la fracción.
	abajo=(2**(2*n))*(n+1)*(factorial(n))**2

	#La fracción dividida.
	final=arriba/abajo
	return final

def ecuacion_p1(t,N,angulo):
	lam=valores_lam()
	#suma=0
	u=np.zeros(N)
	#La función que calculara los valores de nuestra ecuacion.
	for i in range(0,N):
		suma=0
		for n in range(1,6):
			#El valor de r*lambda a usar en esta vuelta.
			xd=(i*lam[n])
			#El valor de nuestras funciones de Bessel.
			J2=special.jv(2,xd)
			J3=special.jv(3,lam[n])

			#La posicion de las sumas
			sumaUp=(J2*np.cos(t*lam[n]))
			sumaDown=(lam[n]**3)*J3

			#El valor final de la suma de todos nuestros valores.
			suma+=sumaUp/sumaDown
		#El valor de la función a r=i.
		u[i]=24*(np.sin(2*angulo)*suma)

	return u

def ecuacion_p2(rho,N):
	alp=valores_lam()
	#suma=0
	u=np.zeros(N)
	#La función que calculara los valores de nuestra ecuación.
	for i in range(0,N):
		suma=0
		for n in range(1,6):
			#El valor de alpha*p para la fución de Bessel J_0.
			xd=rho*alp[n]
			#El valor de z*alpha para la función de sinh(z*alpha).
			xd2=alp[n]*(0.1*i)
			#El valor de nuestras funciones de Bessel.
			J0=special.jv(0,xd)
			#print('J0= ',J0)
			J1=special.jv(1,alp[n])
			#print('J1= ',J1)

			#La posición de las sumas
			sumaUp=J0*np.sinh(xd2)
			#print('Suma Up: ',sumaUp)
			sumaDown=(J1*alp[n])*np.sinh(2*alp[n])
			#print('Suma Down: ',sumaDown)

			#El valor final de la suma de los valores.
			suma+=sumaUp/sumaDown
		#El valor de la función r=i

		u[i]=200*suma

	return u

def ecuacion_p3(z,N,respuesta):
	lam=valores_lam()
	u=np.zeros(N)

	if (respuesta==1):
		for i in range(0,N):
			suma=0
			for n in range(1,6):
				#Conseguir el valor de alpha.
				alp=2*lam[n]
				#Funcion de Bessel.
				J0=special.jv(0,alp*i)
				#Funcion sinh.
				funcion=np.sinh(lam[n]*(5-z))
				#Conseguir la función cn
				cn=c(i,n,alp,lam[n])
				#La suma completa.
				suma+=cn*funcion*J0
			#El valor de u[i]
			u[i]=suma

	else:
		for i in range(0,N):
			suma=0
			for n in range(1,6):
				#Conseguir el valor de alpha.
				alp=lam[n]*(2)
				#Funcion de Bessel.
				J0=special.jv(0,alp*i)
				#Funcion sinh.
				funcion1=np.sinh(lam[n]*(5-z))
				#Conseguir la función cn
				cn=c(i,n,alp,lam[n])
				#La parte1
				parte1=cn*funcion1*J0

				#La funcion sinh para la parte de an.
				funcion2=np.sinh(lam[n]*z)
				#Conseguir la funcion an.
				an=a(i,n,alp,lam[n])
				#La parte 2.
				parte2=an*funcion2*J0

				#La suma total.
				suma+=parte2+parte1
			#El valor de u[i]
			u[i]=suma
	return u

def ecuacion_p4(z,N,ene):
	u=np.zeros(N)
	#Esto es para observar si la función es par. El código presenta un problema
	#pues sin(n*pi/2) donde n=par, ĺa función resulta ser demasiado pequeña
	#(de exponencias 10^{-16}), pero no es igual a 0, por lo que la función
	#presentara valores incorrectos en ciertos momentos.
	#Si el valor z es par, entonces hacemos que u[i]=0.
	if (z%2==0):
		for i in range(0,N):
			u[i]=0
	#Si el numero es no par, entonces procedemos a calcular el código de forma
	#normal. 
	else:
		for i in range(0,N):
			suma=0
			for n in range(1,ene,2):
				valor=(n*math.pi)/2
				I0=special.iv(0,valor*(i))
				I0D=special.iv(0,valor)
				#La parte de arriba de la fracción.
				sumArriba=((-1)**(n+1))*I0
				#La parte de abajo de la fracción.
				sumAbajo=(n*I0D)
				#Suma final.
				suma+=(sumArriba/sumAbajo)*np.sin((n*math.pi/2)*z)
			#El valor de la función u.
			u[i]=(40/math.pi)*suma
	return u


def ecuacion_p5(theta,N,ene):
	u=np.zeros(N)
	valor=np.cos(theta)
	for i in range(0,N):
		suma=0
		#print('Estamos en x={0:.0f}'.format(i))
		for n in range(0,ene):
			#Generamos lo que esta fuera de la fracción.
			prim_parte=(4*n+3)*((i)**(2*n+1))
			#Generamos la sección de la fracción de la solución.
			segun_parte=funcion_factorial(n)
			#Generamos el valor del polinomi de Legendre.
			Legendre=special.lpmv(0,2*n+1,valor)

			#Resolvemos la fracción para n.
			Multi=(prim_parte)*(segun_parte)*Legendre
			#Vamos agregando los valores para la suma con todos los n.
			suma+=Multi
		#Ir agregando los valores a la matriz de u.
		u[i]=60+20*suma


	return u

def solucion():
	tiempo=time() #Para comenzar a contabilizar el tiempo.
	j=0 #Para añadirle digitos a los txt.

	print('------------------------------------------------------------')
	print('Cual problema buscas resolver? Escribe un digito del 1 al 5.')
	p=int(input('Problema '))
	if (1<=p<=5):
		print(' ')
		print('Escogio el problema {0:.0f}.'.format(p))

		print('------------------------------------------------------------')
		print('\n')
		print('-------------------------------------------------------------------')
		print('Decida el valor de distancia (r,\u03C1,x,etc...) que busca obtener.')
		N=int(input('x='))
		N+=1
		if (1<=p<=4):
			print('Decida el valor de tiempo (t,z,etc...) que desea obtener.')
			Te=int(input('t='))
			Te+=1
			print('-------------------------------------------------------------------')
			print('\n')
		else:
			print('-------------------------------------------------------------------')
			print('\n')

		if (p==1):
			print('\n')
			print('Cual angulo quieres usar?')
			angulo=int(input('\u03C0/'))
			for t in range(0,Te):
				u=ecuacion_p1(t,N,angulo)
				#Guardamos los valores de u en un txt.
				escribir=txt(t,u,N,j)
				#Mostramos la gráfica a nuestro t.
				graficar=grafica(t,u,N)
				j+=1
		elif (p==2):
			for rho in range(0,Te):
				u=ecuacion_p2(rho,N)
				#Guardamos los valores de u en un txt.
				escribir=txt(rho,u,N,j)
				#Mostramos la grafica a nuestra posición z.
				graficar=grafica(rho,u,N)
				j+=1
		elif (p==3):
			print('Desea resolver el sistema en steady state?')
			print('Escriba 1 para el steady state, cualquier otro numero para resolver con condiciones de borde.')
			respuesta=int(input())
			for z in range(0,Te):
				u=ecuacion_p3(z,N,respuesta)
				#Guardamos los valores de u en un txt.
				escribir=txt(z,u,N,j)
				#Mostramos la gráfica a nuestra posición z.
				graficar=grafica(z,u,N)
				j+=1
		elif (p==4):
			print('Cuantos valores de n desea tomar en la sumatoria?')
			print('El valor tiene que ser par para evitar problemas con el codigo.')
			ene=int(input('n='))
			if (ene%2==0):
				ene+=1
				for z in range(0,Te):
					#Guardamos el valor de la función calculada.
					u=ecuacion_p4(z,N,ene)
					#Guardamos los valores de u en un txt.
					escribir=txt(z,u,N,j)
					#Mostramos la grafica a nuestra posición de z.
					graficar=grafica(z,u,N)
					j+=1
			else:
				print('Se debe escoger un valor de n par.')
		elif (p==5):
			t=1
			print('Cuantos valores de n desea tomar en la sumatoria?')
			ene=int(input('n='))
			ene+=1
			for factor in range(1,6):
				theta=(math.pi)/factor
				print('Se usara \u03C0/{0:.0f} para este calculo.'.format(factor))
				u=ecuacion_p5(theta,N,ene)
				#Guardamos los valores de u en un txt.
				escribir=txt(theta,u,N,j)
				#Mostramos la grafica a nuestra posición de theta.
				graficar=grafica(t,u,N)
				t+=1
				j+=1
	else:
		print('\n')
		print('El problema escogido debe ser un digito entero entre 1 y 5.')
		print('------------------------------------------------------------')

	print('\n')
	tiempo_calculado=tiempo_total(tiempo)

#Aqui corremos todo el código.
if ( __name__ == '__main__' ):
	solucion=solucion()