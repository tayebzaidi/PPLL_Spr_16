# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 10:17:46 2016

@author: alumno
"""

from multiprocessing import Process, Pipe
import random

def lcr(id, send_canal, recv_canal):
    
    send_canal.send(id)
    while True:
        d = recv_canal.recv()
        print id, "message recieved", d
        
        if d == "halt":
            print id, "halt"
            send_canal.send(d)
            break
        elif d[1] > id:
            print id, "resend id", d
            send_canal.send(d)
        elif d == id:
            print "Leader", id, "FOUND"
            send_canal.send("halt")
            print "LEADER", id, "HALT"
            
            
if __name__=="__main__":
    N = 5
    ids = range(N)
    random.shuffle(ids)
    print "ids", ids
    
    canals = []
    for i in range(N):
        c_recv, c_send = Pipe(duplex=False)
        canals.append((c_recv,c_send))
        
    nodes = []
    for i in range(N):
        nodes.append(Process(target = lcr, args=(ids[i], canals[i][1], canals[(i-1)%N][0])))
    for p in nodes:
        p.start()
    for p in nodes:
        p.join()
    print "Terminamos"