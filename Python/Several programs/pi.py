import __future__ as fut
import math as math
import random as rd
import numpy as np
import pandas as pd
import sys as sys
import matplotlib.pyplot as plt
import seaborn as sns

numero_particulas=1000000

sns.set_style("ticks")

def lanzar_particulas(diametro=1):
    return[(0.5-rd.random())*diametro,(0.5-rd.random())*diametro]

def punto_circulo(punto,diametro):
	return (punto[0])**2+(punto[1])**2<=(diametro/2)**2

def lluvia(numero_particulas,diametro=1,format='png'):
  numero_circulo=0
  suma_pi=0
  dentro_circulo=[]
  fuera_circulo=[]
  pi_calculado=[]
  suma_pi=0
  for i in range(numero_particulas):
    d= (lanzar_particulas(diametro))
    if punto_circulo(d,diametro):
    	dentro_circulo.append(d)
    	numero_circulo+=1
    else:
    	fuera_circulo.append(d)
    pi_calculado.append(4*numero_circulo/(i+1))
  for i in range(1,numero_particulas):
    suma_pi=suma_pi+pi_calculado[i]
  valor_pi=suma_pi/(numero_particulas+1)
  print ("El valor de \u03C0 es:",valor_pi)
  plt.figure()
  plt.title("El valor de \u03C0.")
  plt.scatter(range(1,numero_particulas+1),pi_calculado,color='black', linewidths=0.001, label='Valor de pi')
  plt.xlim(-10,numero_particulas)
  plt.ylim(3.10,3.20)
  plt.xlabel("Particulas")
  plt.ylabel("Valor de \u03C0")
  plt.savefig('graf_pi')
  plt.legend(loc="upper right")
  plt.show()
  return[numero_circulo,numero_particulas]


if __name__== "__main__":
  if len(sys.argv) > 1:
   numero_particulas= eval(sys.argv[ 1 ])
  graficar=lluvia(numero_particulas,format='png')