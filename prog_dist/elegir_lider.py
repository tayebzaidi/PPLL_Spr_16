from multiprocessing import Process, Pipe
import random

def lcr(id, send_canal, recv_canal):
    
    send_canal.send(id)
    while True:
        d = recv_canal.recv()
        if d > id:
            print id, "resend id", d
            send_canal.send(d)
        elif d == id:
            print "Leader", id
            
            
if __name__=="__main__":
    N = 5
    ids = range(N)
    random.shuffle(ids)
    print "ids", ids
    
    canals = []
    for i in range)N=:
        c_recv, c_send = Pipe(duplex=False)
        
    

