# -*- coding: utf-8 -*-
import numpy as np
from numpy.random.mtrand import randint
import random2 as rnd
import math


# Define el cuadrado mágico que solucionaremos nxn
def cuadrado_inicial(n):
    matriz = np.arange(n*n)
    matriz = np.ones(n*n) + matriz 
    np.random.shuffle(matriz)
    # matriz = np.reshape(matriz,(n,n))
    return matriz.astype(int)

# Función de la constante mágica
def constante_magica(n):
    const = n*(n*n+1)/2
    return int(const)

# Función de coste
def coste(vector):
    # print(matriz)
    nsq = vector.size
    n = int(math.sqrt(nsq))
    matriz = np.reshape(vector, (n,n))
    n_magico = constante_magica(matriz.shape[0])
    col_sum = abs(np.sum(matriz,axis=0) - n_magico)
    row_sum = abs(np.sum(matriz,axis=1) - n_magico)
    p_diag_sum = abs(np.trace(matriz) - n_magico)
    s_diag_sum = abs(np.trace(matriz[::-1]) - n_magico)
    diff = sum(col_sum)+sum(row_sum)+p_diag_sum+s_diag_sum
    return (diff.astype(int))

# Función descarte
def descarte(v_grande,v_peq):
    return [i for i in v_grande if i not in v_peq]

# Operador SIC 1 punto
def single_SIC(v1,v2):
    nsq = v1.size
    n = int(math.sqrt(nsq))
    # Desde 1 hasta n^2-1 para que no nos coja los casos en los que la cabeza o la colilla están vacías
    cut = randint(1,nsq-1) 
    # print('Punto de corte: '+str(cut))
    head1 = v1[:cut]
    tail1 = v1[cut:]
    head2 = v2[:cut]
    tail2 = v2[cut:]
    s1 = np.append(head1[::-1],descarte(v2,head1))
    s2 = np.append(descarte(v2,head1),head1[::-1])
    s3 = np.append(head2[::-1],descarte(v1,head2))
    s4 = np.append(descarte(v1,head2),head2[::-1])
    s5 = np.append(tail1[::-1],descarte(v2,tail1))
    s6 = np.append(descarte(v2,tail1),tail1[::-1])
    s7 = np.append(tail2[::-1],descarte(v1,tail2))
    s8 = np.append(descarte(v1,tail2),tail2[::-1])
    return(s1,s2,s3,s4,s5,s6,s7,s8)

# Operador SIC 2 puntos
def double_SIC(v1,v2):
    nsq = v1.size
    n = int(math.sqrt(nsq))
    # Desde 1 hasta n^2-1 para que no nos coja los casos en los que la cabeza o la colilla están vacías
    cut1 = randint(1,nsq-1)
    cut2 = randint(1,nsq-1)
    while cut1==cut2:
        cut2 = randint(1,nsq-1)
    print('Primer punto de corte: '+str(cut1))
    print('Segundo punto de corte: '+str(cut2))  
    head1 = v1[:cut1]
    tail1 = v1[cut2:]
    head2 = v2[:cut1]
    tail2 = v2[cut2:]
    s1 =np.append(np.append(head1[::-1],descarte(descarte(v2,head1),tail1)),tail1[::-1])
    s2 =np.append(np.append(tail1[::-1],descarte(descarte(v2,head1),tail1)),head1[::-1])
    s3 =np.append(np.append(head2[::-1],descarte(descarte(v1,head2),tail2)),tail2[::-1])
    s4 =np.append(np.append(tail2[::-1],descarte(descarte(v1,head2),tail2)),head2[::-1])
    return(s1,s2,s3,s4)

# Operador mutación simple
def single_mutacion(m1):
    n = m1.shape[0]
    v1 = np.reshape(m1,n*n)
    a = randint(n*n-1)
    b = randint(n*n-1)
    while b==a:
        b = randint(n*n-1)
    aux_a = v1[a]
    aux_b = v1[b]
    v1[b] = aux_a
    v1[a] = aux_b
    result = np.reshape(v1,(n,n))
    return result

# Operador mutación cuádruple
def quad_mutacion(m1):
    n = m1.shape[0]
    v1 = np.reshape(m1,n*n)
    a = randint(n*n-1)
    v_a = np.array(range(a,a+4))
    for i in v_a:
        if i>=n*n:
            v_a[i-a]=i-n*n
    # print(v_a)
    b = randint(n*n-1)
    v_b = np.array(range(b,b+4))
    for i in v_b:
        if i>=n*n:
            v_b[i-b]=i-n*n
    while np.in1d(v_a,v_b).any() == True:
        b = randint(n*n-1)
        v_b = np.array(range(b,b+4))
        for i in v_b:
            if i>=n*n:
                v_b[i-b]=i-n*n
    # print(v_b)
    aux_a = v1[v_a]
    aux_b = v1[v_b]
    j=0
    for i in v_a:
        v1[i]=aux_b[j]
        j+=1
    j=0
    for i in v_b:
        v1[i]=aux_a[j]
        j+=1
    result = np.reshape(v1,(n,n))
    return result

# Selección del mejor entre dos competidores del torneo
def peguense(m1,m2):
    return m2 if coste(m1)>coste(m2) else m1

# Define la función de torneo que gestionará cómo se organizan los enfrentamientos 
def torneo(genes, p):
    ganadores = genes.copy()
    
    while ganadores.shape[0] > p:
        #  nos aseguramos de que sea divisible entre p
        while ganadores.shape[0] % p != 0:
            ganador =  peguense(ganadores[0], ganadores[1])
            ganadores = ganadores[2:]
            subset = np.vstack((ganador, ganadores))

        # t de cada subset
        t_subset = ganadores.shape[0]//p
        # creamos los subsets
        print(ganadores)
        for i in range(0,ganadores.shape[0], t_subset):
            subset = ganadores[i:i+t_subset]
            print(subset)
            while subset.shape[0] != 1: 
                ronda = []
                if subset.shape[0] % 2 != 0:
                    print(subset)
                    ganador =  peguense(subset[0], subset[1])
                    subset = subset[2:]
                    ganador = np.reshape(ganador, (1,ganador.shape[0], ganador.shape[1]))
                    subset = np.vstack((ganador, subset))
                
                for j in range(0, subset.shape[0], 2):
                    ganador =  peguense(subset[j], subset[j+1])
                    ronda.append(ganador)
                subset = np.array(ronda)
            if finalistas:
                finalistas = np.vstack((finalistas, subset))
            else:
                finalistas = subset # mal

        ganadores = finalistas

    return ganadores

# Función de selección proporcional
def ruleta(genes, p):
    aptitudes = [1/coste(i) for i in genes]
    sum_aptitudes = sum(aptitudes)
    probabilidades = [i/sum_aptitudes for i in aptitudes]
    sol = []
    for _ in range(p):
        n_random = np.random.random(1)
        acc = 0
        for i in probabilidades:
            acc += i
            if n_random <= acc:    
                sol.append(genes[probabilidades.index(i)])
                break
    return np.array(sol)

# p tiene que ser un número de la forma 2^n por temas de eficiencia computacional
def main(n, p, prob_mutation, max_pasos):
    # Inicialización
    genes = [cuadrado_inicial(n) for _ in range(p)]
    genes = np.array(genes)
    np.random.shuffle(genes)
    n_gen = []
    pasos = 0
    optimo = False
    solution = None
    while pasos < max_pasos or optimo:
        # Crea los hijos y los añade al pool de genes que tenemos 
        for i in range(0, genes.shape[0], 2):
            '''(cut1, cut2) = randint(1, n*n, sizs)
            print('GENES 1')
            print(genes[i+1])
            s = double_SIC(genes[i], genes[i+1], cut1, cut2)'''
            cut = randint(1, n*n)
            s = single_SIC(genes[i], genes[i+1],cut)
            n_gen = n_gen + list(s)
     
        genes = np.concatenate((genes, n_gen))
        np.random.shuffle(genes)

        # Torneo 
        genes = torneo(genes, p)

        # Ruleta 
        #genes = ruleta(genes,p)

        # Mutación
        for i in range(genes.shape[0]):
            n_rand = np.random.random()
            if n_rand <= prob_mutation:
                genes[i] = single_mutacion(genes[i])
        
        # Comprobación 
        for i in genes:
            if coste(i) == 0:
                solution = i
                optimo = True
                break
        
        # print('Iteración ' + str(pasos))
        for i in genes:
            print(i, coste(i))
        # Incremento de los pasos dados
        pasos += 1

    if solution != None:
        return solution
    
    else:
        return genes


# Debugeo
n=4

ejemplo1 = cuadrado_inicial(n)
ejemplo2 = cuadrado_inicial(n)

print('Cuadrados iniciales de n='+str(n))
print(ejemplo1)
print(ejemplo2)

# print('Constante magica: '+str(constante_magica(n)))
# print('Coste del cuadrado inicial: '+str(coste(ejemplo1)))

print('Cruce SIC simple')
print(single_SIC(ejemplo1,ejemplo2))

print('Cruce SIC doble')
print(double_SIC(ejemplo1,ejemplo2))