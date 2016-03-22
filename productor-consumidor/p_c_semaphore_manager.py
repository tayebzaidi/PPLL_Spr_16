from multiprocessing import Process
from multiprocessing import BoundedSemaphore
from multiprocessing import current_process
from multiprocessing import Manager

import time, random

N = 10
K = 5

def p(almacen,poner,tomar): 
    for v in range(N):
        print current_process().name, "produciendo"
        time.sleep(random.random()/2)
        poner.acquire()
        almacen.append(current_process().name[-1:]+"."+str(v)	)	
        print current_process().name, "almacenando", v
        tomar.release()                 

def c(almacen,poner,tomar):
     for v in range(N):
        tomar.acquire()        
        print current_process().name, "desalmacenando"
        dato = almacen.pop(0)
        poner.release()
        print current_process().name, "consumiendo", dato  
        time.sleep(random.random()/2)
        
if __name__ == "__main__":
    poner = BoundedSemaphore(K)  
    tomar = BoundedSemaphore(K)
    for i in range(K):
        tomar.acquire()

    manager = Manager()
    l = manager.list()

    print "almacen inicial", l[:]

    productor1 = Process(target=p, name="productor1", args=(l,poner,tomar))
    productor2 = Process(target=p, name="productor2", args=(l,poner,tomar))
    consumidor1 = Process(target=c, name="consumidor1", args=(l,poner,tomar))
    consumidor2 = Process(target=c, name="consumidor2", args=(l,poner,tomar))

    productor1.start()
    consumidor1.start()
    productor2.start()
    consumidor2.start()
    
    
    productor1.join()
    consumidor1.join()
    productor2.join()
    consumidor2.join()
    
    print "fin"
    
