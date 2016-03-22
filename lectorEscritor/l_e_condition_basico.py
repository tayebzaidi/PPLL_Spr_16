from multiprocessing import Process
from multiprocessing import Condition
from multiprocessing import Manager
from multiprocessing import current_process
import time, random

def lector(c,nu,K):
    for x in range(K):
        c.acquire()
        while (nu[0] > 0):
            print "lector"+current_process().name+" espera............."
            c.wait()
        nu[1] = nu[1] + 1
        c.release()
                    
        print "Lector "+current_process().name+" lee de la DB", x, "Estado: escritores", nu[0], "lectores", nu[1] 
        time.sleep(random.random())
        
        c.acquire()
        nu[1] = nu[1] - 1
        if nu[1] == 0:
            c.notify_all()
        c.release()

        print "Lector "+current_process().name+" piensa en lo que ha leido", x

def escritor(c,nu,K):    
    for x in range(K):
        print "Escritor "+current_process().name+"  piensa lo que va a escribir", x

        c.acquire()
        while (nu[0] > 0 or nu[1] > 0):
            print "escritor "+current_process().name+" espera................."
            c.wait()
        nu[0] = nu[0] + 1
        c.release()
            
        print "Escritor "+current_process().name+" escribe en la DB", x, "Estado: escritores", nu[0], "lectores", nu[1] 
        time.sleep(random.random())

        c.acquire()
        nu[0] = nu[0] - 1
        c.notify_all()
        c.release()

if __name__ == '__main__':
    NL = 5 #numero lectores
    NE = 2 #numero escritores
    K = 5 #numero iteraciones

    manager = Manager()
    nu = manager.list([0,0]) #numero de usuarios, nu[0] escritores, nu[1] lectores.
    c = Condition()

    l = []
    for x in range(NL):
        l.append(Process(target=lector, args=(c, nu, K)))
    e = []
    for x in range(NE):        
        e.append(Process(target=escritor, args=(c, nu, K)))

    for x in e+l:
        x.start()
    for x in e+l:
        x.join()
