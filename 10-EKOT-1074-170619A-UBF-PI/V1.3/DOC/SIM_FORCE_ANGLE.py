#pa ver como jala la asistencia segun el angulo del brazo.
#import matplotlib
import matplotlib.pyplot as plt
import numpy as np


#k es constante del resorte.
#r es el radio del brazo de asistencia.
#i es la pretension del resorte.
#th es el angulo del brazo.
def asiste(k,r,i,th):
    L=r*th
    if th<=(np.pi/2):
        f=(k*(L+i))
    else:
        f=(np.cos(th))*(k*(L+i))
    return float(f)

#guardamos todos los datos en una matriz.
def calculo():
    #lo ideal seria un slider, pero aqui meter los parametros.
    #constante resorte (kg/mm)
    k = 0.333
    #radio brazo asistencia(mm)
    r = 80
    #pretension(m)
    i = 0
    #se inician las variables.
    th = 0
    #print (th)
    cont = 0
    #vectores vacios para guardar los datos.
    grados = np.array([])
    datos = np.array([])
    #calculamos y llenamos vectores.
    while th<(np.pi):
        datos = np.append(datos,abs(asiste(k,r,i,th)))
        #print(cont)
        #print(th)
        #print(datos[cont])
        print(grados)
        grados = np.append(grados,th)
        th = th + (np.pi/8)
        cont += 1
    return grados, datos

#hacemos la grafica
def mapeo():
    ejeX, ejeY = calculo()
    plt.plot(ejeX, ejeY)
    #etiquetamos.
    plt.xlabel("Angulo(R)")
    plt.ylabel("Asistencia (N)")
    plt.show()

def main():
    mapeo()

if __name__ == "__main__":
    main()
