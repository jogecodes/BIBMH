# -*- coding: utf-8 -*-
import numpy as np
from numpy.random.mtrand import randint
import random2 as rnd


# Define el cuadrado mágico que solucionaremos nxn
def cuadrado_inicial(n):
    matriz = np.arange(n*n)
    matriz = np.ones(n*n) + matriz 
    np.random.shuffle(matriz)
    matriz = np.reshape(matriz,(n,n))
    return matriz.astype(int)

# Función de la constante mágica
def constante_magica(n):
    return n*(n*n+1)/2

# Función de coste
def coste(matriz):
    n_magico = constante_magica(matriz.shape[0])
    col_sum = abs(np.sum(matriz,axis=0) - n_magico)
    row_sum = abs(np.sum(matriz,axis=1) - n_magico)
    p_diag_sum = abs(np.trace(matriz) - n_magico)
    s_diag_sum = abs(np.trace(matriz[::-1]) - n_magico)
    diff = sum(col_sum)+sum(row_sum)+p_diag_sum+s_diag_sum
    return (diff.astype(int))

def descarte(v_grande,v_peq):
    return [i for i in v_grande if i not in v_peq]

# Operador de cruce Luis
def crucelui(m1,m2):
    # n = m1.shape[0]
    num = rnd.choice(rnd.choice(m1))
    result1 = np.where(m1 == num)
    result2 = np.where(m2 == num)
    coord1 = [result1[0][0],result1[1][0]]
    coord2 = [result2[0][0],result2[1][0]]
    return (num,coord1,coord2)

# Operador SIC 1 punto
def single_SIC(m1,m2,cut):
    n = m1.shape[0]
    v1 = np.reshape(m1,n*n)
    v2 = np.reshape(m2,n*n)
    # Desde 1 hasta n^2-1 para que no nos coja los casos en los que la cabeza o la colilla están vacías
    head1 = v1[:cut]
    tail1 = v1[cut:]
    head2 = v2[:cut]
    tail2 = v2[cut:]
    s1 = np.reshape(np.append(head1[::-1],descarte(v2,head1)),(n,n))
    s2 = np.reshape(np.append(descarte(v2,head1),head1[::-1]),(n,n))
    s3 = np.reshape(np.append(head2[::-1],descarte(v1,head2)),(n,n))
    s4 = np.reshape(np.append(descarte(v1,head2),head2[::-1]),(n,n))
    s5 = np.reshape(np.append(tail1[::-1],descarte(v2,tail1)),(n,n))
    s6 = np.reshape(np.append(descarte(v2,tail1),tail1[::-1]),(n,n))
    s7 = np.reshape(np.append(tail2[::-1],descarte(v1,tail2)),(n,n))
    s8 = np.reshape(np.append(descarte(v1,tail2),tail2[::-1]),(n,n))
    return(s1,s2,s3,s4,s5,s6,s7,s8)

# Operador SIC 2 puntos
def double_SIC(m1,m2,cut1,cut2):
    n = m1.shape[0]
    v1 = np.reshape(m1,n*n)
    v2 = np.reshape(m2,n*n)
    # Desde 1 hasta n^2-1 para que no nos coja los casos en los que la cabeza o la colilla están vacías
    head1 = v1[:cut1]
    # center1 = v1[cut1:cut2] No es necesario
    tail1 = v1[cut2:]
    head2 = v2[:cut1]
    # center2 = v2[cut1:cut2] No es necesario
    tail2 = v2[cut2:]
    s1 = np.reshape(np.append(np.append(head1[::-1],descarte(descarte(v2,head1),tail1)),tail1[::-1]),(n,n))
    s2 = np.reshape(np.append(np.append(tail1[::-1],descarte(descarte(v2,head1),tail1)),head1[::-1]),(n,n))
    s3 = np.reshape(np.append(np.append(head2[::-1],descarte(descarte(v1,head2),tail2)),tail2[::-1]),(n,n))
    s4 = np.reshape(np.append(np.append(tail2[::-1],descarte(descarte(v1,head2),tail2)),head2[::-1]),(n,n))
    return(s1,s2,s3,s4)

# Operador mutación
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

def quad_mutacion(m1):
    n = m1.shape[0]
    v1 = np.reshape(m1,n*n)
    a = randint(n*n-1)
    v_a = np.array(range(a,a+4))
    for i in v_a:
        if i>=n*n:
            v_a[i-a]=i-n*n
    print(v_a)
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
    print(v_b)
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

# Define la selección del mejor entre dos competidores del torneo
def peguense(m1,m2):
    return m2 if coste(m1)>coste(m2) else m1

# Define la función de torneo que gestionará cómo se organizan los enfrentamientos 
def torneo(genes, p):
    g_trabajo = np.copy(genes)
    ganadores = []

    while g_trabajo.shape[0] != p:
        m1_index = np.random.choice(range(g_trabajo.shape[0]))
        m1 = g_trabajo[m1_index]
        g_trabajo = np.delete(g_trabajo, m1_index, axis=0)
        print(g_trabajo)
        m2_index = np.random.choice(range(g_trabajo.shape[0]))
        m2 = g_trabajo[m2_index]
        g_trabajo = np.delete(g_trabajo, m2_index, axis=0)
        print("m1")
        print(m1)
        print("m2")
        print(m2)
        ganadores.append(peguense(m1, m2))
        print(ganadores)
        print(g_trabajo)
    
    return np.array(ganadores)

# Define la función de relección proporcional
def ruleta(genes, p):
    aptitudes = [1/coste(i) for i in genes]
    sum_aptitudes = sum(aptitudes)
    probabilidades = [i/sum_aptitudes for i in aptitudes]
    sol = []
    for _ in range(p):
        n_random = np.random.random(1)
        print(n_random)
        acc = 0
        for i in probabilidades:
            acc += i
            if n_random <= acc:    
                sol.append(genes[probabilidades.index(i)]) 
                break
        
    return np.array(sol)

# p tiene que ser un número de la forma 2^n por temas de eficiencia computacional
def main(n, p):
    genes = [cuadrado_inicial(n) for _ in range(p)]
    genes = np.array(genes)
    np.random.shuffle(genes)
    n_gen = []
    for i in range(0, genes.shape[0], 2):
        (cut1, cut2) = randint(1, n*n, size = 2)
        s = double_SIC(genes[i], genes[i+1], cut1, cut2)
        n_gen = n_gen + s[0] + s[1] + s[2] + s[3]
    np.append(genes, n_gen)
    np.random.shuffle(genes)
# Torneo


ejemplo1 = cuadrado_inicial(4)
ejemplo2 = cuadrado_inicial(4)


# print('----------------------------')
# print(peguense(ejemplo1,ejemplo2))
# print('----------------------------')
# print(ejemplo1)
# print('----------------------------')
# print(ejemplo2)
# print(ejemplo1)
# print(ejemplo2)
# print("--------------")
# var = double_SIC(ejemplo1, ejemplo2,3,7)
# for i in var[:-1]:
#     print (i)
#     print("--------------")
# print(var[-1])
# ejemplo1 = quad_mutacion(ejemplo1)