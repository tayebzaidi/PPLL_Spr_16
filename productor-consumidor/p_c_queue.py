from multiprocessing import Process
from multiprocessing import Queue
from multiprocessing import current_process

from time import sleep
from random import random

N = 10
K = 3

def p(almacen):
    for v in range(N,2*N):
        print current_process().name, "produciendo"
        sleep(random()/3)
        almacen.put(v,block=True)
        print current_process().name, "almacenando", v
       

def c(almacen):
    for v in range(N):
        print current_process().name, "desalmacenando"
        dato = almacen.get(block=True)
        print current_process().name, "consumiendo", dato
        sleep(random()/3)
         
if __name__ == "__main__":

    almacen = Queue(K)
    print "almacen inicial", almacen

    productor = Process(target=p, name="productor", args=(almacen,))
    consumidor = Process(target=c, name="consumidor", args=(almacen,))

    consumidor.start()
    productor.start()
    
   
