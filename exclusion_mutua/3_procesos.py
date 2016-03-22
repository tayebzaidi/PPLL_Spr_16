
from multiprocessing import Process
from multiprocessing import current_process
from multiprocessing import Value



def f(c):
    for i in range(5):
        c.value = c.value + 1
        print "hola soy", current_process().pid, "vuelta", i, "contador", c.value 

if __name__ == "__main__":
    N = 8
    lp = []
    c = Value('i',0)
    for i in range(N):
        lp.append(Process(target=f, args=(c,)))

    print "Valor inicial del contador", c.value
    for p in lp:
        p.start()

    
