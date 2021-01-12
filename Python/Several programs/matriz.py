#-------------------------------------------------------------------------#
# Este código fue realizado para resolver un sistema lineal de ecuaciones #
# representadas en matrices. Esto es para poder obtener los valores de    #
# temperatura de un sistema.                                              #
#                                                                         #
#                                                                         #
# Este programa esta realizado para la materia de Métodos Matématicos de  #
# la Física II, como tarea independiente.                                 #
#                                                                         #
# Hecho por Ricardo Leal.                                                 #
# emal: ricardo.lealpz@gmail.com                          Fecha: 29/10/20 #
#-------------------------------------------------------------------------#

#-----------------------#
#Importar las librerias.#
#-----------------------#

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from time import time

#-------------------------------------------------------------------#
#La función únicamente representa el tiempo de ejecución del código.#
#-------------------------------------------------------------------#

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

#-------------------------------------------------------------------------#
#La siguiente función nos mostrara la matriz A y b visualmente una vez le #
#agregaramos todos los terminos.                                          #
#-------------------------------------------------------------------------#

def matriz_visual(matriz,b,n):
	print("Su matriz es:")
	for i in range(0,n):
		print("| ",end="")
		for j in range(0,n):
			print(matriz[i,j]," ",end="")
		if (i==5):
			print("| |T[{0:.0f}]|".format(i+1)," = |", b[i]," ",end="")
			print("|\n")
		else:
			print("| |T[{0:.0f}]|".format(i+1),"   |", b[i]," ",end="")
			print("|\n")
	print("---------------------------------------------------")
	print("\n")

#---------------------------------------------------------------------#
#La siguiente función es casi identica a la pasada, pero esta vez para#
#la matriz solución del sistema.                                      #
#---------------------------------------------------------------------#

def solucion_visual(Tsol,n):
	print("Su solucion es:")
	for i in range(0,n):
		if (i==5):
			print("|T[{0:.0f}]|".format(i+1)," = |",Tsol[i],"|",end="")
			print("\n")
		else:
			print("|T[{0:.0f}]|".format(i+1),"   |",Tsol[i],"|",end="")
			print("\n")
	print("\n")

#-------------------------------------------------------------------#
#La siguiente función nos permitira agregarle valores a la matriz A.#
#-------------------------------------------------------------------#

def matriz_a(n):
	x=0
	matriz=np.zeros((n,n))
	print("------------------------------------")
	print("Asigne los valores para la matriz A.")
	for i in range(0,n):
		x+=1
		y=0
		print("Estamos en la columna {0:.0f}: ".format(x))	
		for j in range(0,n):
			y+=1
			matriz[i,j]=input("Ingrese el valor para la fila {0:.0f}: ".format(y))
		print("\n")
	print("-----------------------------------")
	print("\n")
	return matriz

#-------------------------------------------------------------------#
#La siguiente función nos permitira agregarle valores a la matriz b.#
#-------------------------------------------------------------------#

def matriz_b(n):
	b=np.zeros(n)
	x=0
	print("------------------------------------")
	print("Asigne los valores para su matriz b.")
	for i in range(0,n):
		x+=1
		b[i]=input("Ingrese el valor para la fila {0:.0f}: ".format(x))
	print("------------------------------------")
	print("\n")
	return b

#-------------------------------------------------------------------#
#La siguiente función nos va a permitir calcular la matriz solución.#
#-------------------------------------------------------------------#

def solucion(matriz,b,n):
	Tsol=np.zeros(n)
	Tsol=np.linalg.solve(matriz,b)
	return Tsol

#------------------------------------------------------------------------#
#La siguiente función únicamente gráficara los resultados de la solución.#
#------------------------------------------------------------------------#

def graficar(Tsol,n):
	sns.set_style("ticks")
	x=np.zeros(n)
	for i in range(0,n):
		x[i]=i+1
	plt.figure()
	plt.plot(x,Tsol,'--b')
	plt.title("Solución del sistema para x={0:.0f} metros.".format(n))
	plt.xlabel('Distancia recorrida.')
	plt.ylabel('Temperatura del sistema')
	plt.grid()
	plt.show()

#-------------------------------------------#
#Generamos un txt con los valores obtenidos.#
#-------------------------------------------#

def txt(Tsol,n):
	t1=open("valores_obtenidos.txt","w")

	for i in range(0,n):
		t1.write(str(i+1)); t1.write(" "); t1.write(str(Tsol))
		t1.write("\n")

	t1.close()

#-------------------------------------------------------------------------#
#La siguiente función es la que coloca ciertos mentajes, ademas de que nos#
#permite ir llamando las funciones anteriores en el orden que busquemos.  #
#-------------------------------------------------------------------------#

def matrices():
	tiempo=time() #Aqui solo le pedimos que comience a contar el tiempo.

	print("--------------------------------------------------------------")
	print("Este código esta hecho para resolter un sistema de matrices.")
	print(" ")
	print("Código hecho para Métodos Matemáticos de la Física II.")
	print("--------------------------------------------------------------")
	print("\n")


	#-------------------------------------------------#
	#Pedimos al usuario la potencia de nuestra matriz.#
	#-------------------------------------------------#

	print("---------------------------------------------")
	valor=input("Escribe la dimension de tu matriz cuadrada:")
	print("---------------------------------------------")
	print("\n")
	n=int(valor)

	#---------------------------#
	#Generamos nuestra matriz A.#
	#---------------------------#

	matriz=matriz_a(n)

	#---------------------------#
	#Generamos nuestra matriz b.#
	#---------------------------#

	b=matriz_b(n)

	#---------------------------#
	#Mostramos las matrices.    #
	#---------------------------#

	mostrar_matriz=matriz_visual(matriz,b,n)

	#Checamos que el usuario busque seguir con la solución.

	pregunta=print("¿Desea continuar con este sistema de matrices?.")
	respuesta=int(input("Escriba 1 para si, cualquier otro número para no: "))

	if (respuesta==1):

		#-----------------------------#
		#Generamos la matriz solución.#
		#-----------------------------#

		Tsol=solucion(matriz,b,n)
		mostrar_solucion=solucion_visual(Tsol,n)
		
		#Graficamos.
		grafica=graficar(Tsol,n)
		escribir_txt=txt(Tsol,n)
		tiempo_calculado=tiempo_total(tiempo)

	else:
		tiempo_calculado=tiempo_total(tiempo)

#corremos todo el código.
if ( __name__ == '__main__' ):
	solucion=matrices()