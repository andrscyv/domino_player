import matplotlib.pyplot as plt
import numpy as np
from math import comb

def pos(t):
    f = 7-t
    s = 28 - 4*t
    return comb(s -f,f)*comb(s-2*f,f)

if __name__ == "__main__":
    # Mcts es correcto
    x1 = [ 1, 5, 20, 60, 100, 250]
    y1 = np.array([0.544, 0.812, 0.909, 0.961, 0.962, 0.967])
    plt.plot(x1,y1*100, '--bo', )
    plt.ylabel('Porcentaje de victorias')
    plt.xlabel('Número de iteraciones en MCTS')
    plt.title('MCTS con información perfecta v.s. Greedy')
    plt.show() 
    #Qué tan sensible es mcts a params
    x2 = [20, 60, 100, 250, 300, 350, 400, 500]
    y2 = [0.176, 0.297, 0.344, 0.486, 0.556, 0.496, 0.514, 0.571]
    plt.plot(x2,np.array(y2)*100, '--bo', )
    plt.ylabel('Porcentaje de victorias')
    plt.xlabel('Número de iteraciones en MCTS')
    plt.title('MCTS con información perfecta v.s. MCTS con 250 iteraciones')
    plt.show() 

    # Número de posibles escenarios
    # el numero de fickas del jugador k = 7, 6, ..., 1
    # los demas jugadores tienen (28 - k)/3 fichas si nadie ha pasado
    # el numero de escenarios es [(28-k) elige k] * [(28 - 2k) elige k]
    x3 = range(8)
    y3 = [ pos(x) for x in x3]
    print(y3)
    plt.plot(x3,np.array(y3), '--bo', )
    plt.ylabel('Escenarios posibles')
    plt.xlabel('Turno')
    plt.title('Escenarios posibles por turno')
    plt.show() 
    #sin primer valor
    x4 = range(1,8)
    y4 = [ pos(x) for x in x4]
    print(y4)
    plt.plot(x4,np.array(y4), '--bo', )
    plt.ylabel('Escenarios posibles')
    plt.xlabel('Turno')
    plt.title('Escenarios posibles por turno')
    plt.show() 
