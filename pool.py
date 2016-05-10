# -*- coding: utf-8 -*-

"""
Ejemplo muy sencillo de uso del Pool de multiprocessing
"""

from multiprocessing import Pool
from time import time
import random

#Prueba con diferentes funciones de mapeo para ver su repercusión en
# el tiempo de ejecución
def f(n):
    sum = 0
    for i in xrange(n*n):
        sum += i
    return f

#Prueba diferentes valores de K para ver las diferencias en el
#tiempo de ejecución.

K = 2000
l = range(3,10)
random.shuffle(l)
print l
for i in l:
    pool = Pool(i)

    #print "regular  map"
    #init_time = time()
    #map(f,range(K))
    #print time()-init_time
    
    print "parallel map: ", i, " cores"
    init_time = time()
    pool.map(f,range(K))
    print time()-init_time
