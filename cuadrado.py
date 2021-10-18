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

# Operador de cruce Luis
def crucelui(m1,m2):
    # n = m1.shape[0]
    num = rnd.choice(rnd.choice(m1))
    result1 = np.where(m1 == num)
    result2 = np.where(m2 == num)
    coord1 = [result1[0][0],result1[1][0]]
    coord2 = [result2[0][0],result2[1][0]]
    return (num,coord1,coord2)

def descarte(v_grande,v_peq):
    return [i for i in v_grande if i not in v_peq]

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
    center1 = v1[cut1:cut2]
    tail1 = v1[cut2:]
    head2 = v2[:cut1]
    center2 = v2[cut1:cut2]
    tail2 = v2[cut2:]
    s1 = np.reshape(np.append(np.append(head1[::-1],descarte(descarte(v2,head1),tail1)),tail1[::-1]),(n,n))
    s2 = np.reshape(np.append(np.append(tail1[::-1],descarte(descarte(v2,head1),tail1)),head1[::-1]),(n,n))
    s3 = np.reshape(np.append(np.append(head2[::-1],descarte(descarte(v1,head2),tail2)),tail2[::-1]),(n,n))
    s4 = np.reshape(np.append(np.append(tail2[::-1],descarte(descarte(v1,head2),tail2)),head2[::-1]),(n,n))
    return(s1,s2,s3,s4)


ejemplo1 = cuadrado_inicial(3)
ejemplo2 = cuadrado_inicial(3)

print(ejemplo1)
print(ejemplo2)
print("--------------")
var = double_SIC(ejemplo1, ejemplo2,3,6)
for i in var[:-1]:
    print (i)
    print("--------------")
print(var[-1])
