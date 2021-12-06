import numpy as np
def torneo(genes, p):
    ganadores = genes.copy()

    while len(ganadores) > p:
        #  nos aseguramos de que sea divisible entre p
        while len(ganadores) % p != 0:
            ganador =  max(ganadores[0], ganadores[1])
            ganadores = ganadores[2:]
            ganadores = [ganador] + ganadores

        # inicializamos finalistas
        finalistas = []
        # t de cada subset
        t_subset = len(ganadores)//p
        # creamos los subsets
        for i in range(0,len(ganadores), t_subset):
            subset = ganadores[i:i+t_subset]
            while len(subset) != 1: 
                ronda = []
                if len(subset) % 2 != 0:
                    ganador =  max(subset[0], subset[1])
                    subset = subset[2:]
                    subset = [ganador] + subset
                
                for j in range(0, len(subset), 2):
                    ganador =  max(subset[j], subset[j+1])
                    ronda.append(ganador)
                subset = ronda
            finalistas = finalistas + subset

        ganadores = finalistas

    return ganadores





a = [[1,2,3,4],[1,2,3,4]]
a = np.array(a)
b = np.array([1,2,3,4])
c = np.vstack((a,np.reshape(b, (1,4)))) 

print(c)