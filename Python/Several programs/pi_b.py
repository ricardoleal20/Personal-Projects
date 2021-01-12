import __future__ as fut
import random as rd
import numpy as np
import pandas as pd
import sys as sys
import matplotlib.pyplot as plt
import seaborn as sns

numero_movimientos=1000000
delta=0.01 #El cambio en las posiciones
x=0.4 #posicion inicial en x
y=0.3 #Posicion inicial en y

sns.set_style("ticks")
#sns.lineplot()

def calcular(numero_movimientos,x,y,delta,format='png'):
  it=1
  j=0
  i=[]
  pi=[]
  suma_pi=0
  while (it<=numero_movimientos): 
    dx=rd.uniform(-delta,delta)
    dy=rd.uniform(-delta,delta)  
    x+=dx
    y+=dy
    it+=1    
    circulo=x**2+y**2
    if((abs(x)<=1)and(abs(y)<=1)):
        if(circulo<1):
         j+=1
        valor_pi=4*j/it
        pi.append(valor_pi)
        i.append(it)
    else: 
        x-=dx
        y-=dy
        it-=1
  for i in range(1,numero_movimientos):
    suma_pi=suma_pi+pi[i]
  calculado_pi=suma_pi/(numero_movimientos+1)
  print ("El valor de \u03C0 es:",calculado_pi)
  plt.figure()
  plt.title("Valor de \u03C0")
  plt.scatter(range(1,numero_movimientos+1),pi,color='black', linewidths=0.001, label='Valor de pi')
  plt.xlabel("Particulas")
  plt.ylabel("Valor de \u03C0")
  plt.savefig('graf_pi')
  plt.legend(loc="upper right")
  plt.show()
  return[numero_movimientos]


if __name__== "__main__":
  if len(sys.argv) > 1:
   numero_movimientos= eval(sys.argv[ 1 ])
  graficar=calcular(numero_movimientos,x,y,delta,format='png')


