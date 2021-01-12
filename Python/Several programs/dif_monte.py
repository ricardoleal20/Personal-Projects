import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random as random
sns.set_style('whitegrid')

def cuadrado(L):
    #Vertices del cuadrado.
    xt=np.zeros(5)
    yt=np.zeros(5)
    xt[0]=-L;xt[1]=L;xt[2]=L;xt[3]=-L;xt[4]=xt[0]
    yt[0]=-L;yt[1]=-L;yt[2]=L;yt[3]=L;yt[4]=yt[0]
    return xt,yt
def distancia(x,y,i):
    return np.sqrt((x[i]-x[i-1])**2+(y[i]-y[i-1])**2)

def monte_carlo(N,L):
    x=np.zeros(N);y=np.zeros(N)
    D=L
    x[0]=0
    y[0]=0 #El punto inicial.
    #El ciclo while para las N iteraciones
    i=1
    while (i<=(N-1)):
    #for i in range(1,N-1):
        #Se escoge aleatoriamente una celda anterior.
        num=random.randint(0,i-1)
        #Se escoge aleatoriamente una de las 8 posibilidades.
        mx=random.randint(-1,1) 
        my=random.randint(-1,1)
        #Nos aseguramos de descartar que se quede donde mismo.
        l=random.randint(1,2)
        if (l==1):
        	mx=-1
        	my=random.randint(-1,1)
        	if (my==-1):
        		mx=0
        elif (l==2):
        	mx=1
        	my=random.randint(-1,1)
        	if (my==1):
        		mx=0
        #Ahora, creamos la nueva posicion que es x[i] y y[i].
        x[i]=x[num]+mx;y[i]=y[num]+my
        #Calculamos la distancia con la funcion distancia.
        d=distancia(x,y,i)
        if (d>D): #Comprobamos que la distancia sea aceptable.
            x[i]=x[i-1]; y[i]=y[i-1]
        if ((-L/2)<x[i]<(L/2)):
            if ((-L/2)<y[i]<(L/2)):
                i+=1
        else:
            i=N-1
    return x,y

def graf(x,y,L):
    xt,yt=cuadrado(L/2)
    plt.figure()
    sns.scatterplot(x,y)
    plt.plot(xt,yt,'r',lw=3)
    plt.savefig('d1.png')
    plt.show()
def txt(x,y,N):
    t1=open("difusion.txt","w")

    for i in range(0,N-1):
        t1.write(str(x[i])); t1.write(" "); t1.write(str(y[i]))
        t1.write("\n")

    t1.close()

N=int(1e2) #Debe terminar en 1, para que el código funcione.
L=30

x,y=monte_carlo(N,L)
grafica=graf(x,y,L)