from multiprocessing import Process
from multiprocessing import Lock
from multiprocessing import current_process
from multiprocessing import Value

N = 10

def p(almacen, poner, tomar):
    for v in range(N):
        print current_process().name, "produciendo", v
        poner.acquire()
        almacen.value = v    
        print current_process().name, "almacenando", v
        tomar.release()

def c(almacen, poner, tomar):
    for v in range(N):
        tomar.acquire()        
        dato = almacen.value
        print current_process().name, "desalmacenando", dato
        poner.release()
        print current_process().name, "consumiendo", dato
        
if __name__ == "__main__":

    poner = Lock()  #observa que no basta un unico lock!!
    tomar = Lock()
    tomar.acquire()

    almacen = Value('i', -1)
    print "almacen inicial", almacen

    productor = Process(target=p, name="productor", args=(almacen,poner,tomar))
    consumidor = Process(target=c, name="consumidor", args=(almacen,poner,tomar))

    productor.start()
    consumidor.start()
    
