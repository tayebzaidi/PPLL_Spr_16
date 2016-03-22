from multiprocessing import Process
from multiprocessing import Condition
from multiprocessing import current_process
from multiprocessing import Manager
import time
import random

N = 10
K = 3
def delay(factor = 5):
    time.sleep(random.random()/factor)
    
def p(almacen,control): 
    for v in range(N):
        print current_process().name, "produciendo"
        control.acquire()
        while len(almacen) == K:
            print current_process().name, "esperando..."
            control.wait()
            print current_process().name, "despertando..."
        almacen.append(current_process().name[-1:]+"."+str(v)	)	
        print current_process().name, "almacenando", current_process().name[-1:]+"."+str(v)	
        control.notify()
        control.release() 
        delay()
                        
def c(almacen,control):
     for v in range(N):
        control.acquire()        
        while len(almacen) == 0:
            print current_process().name, "esperando.."
            control.wait()
            print current_process().name, "despertando..."
        print current_process().name, "desalmacenando"
        dato = almacen.pop(0)
        control.notify()
        control.release()
        print current_process().name, "consumiendo", dato  
        delay()
        
if __name__ ==  "__main__":

    control = Condition()
    manager = Manager()
    l = manager.list()
    print "almacen inicial", l[:]

    productor1 = Process(target=p, name="productor1", args=(l,control))
    consumidor1 = Process(target=c, name="consumidor1", args=(l,control))
   
    productor1.start()
    consumidor1.start()
       
    productor1.join()
    consumidor1.join()
   
