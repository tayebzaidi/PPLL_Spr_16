# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 10:47:49 2016

@author: alumno
"""
def client(K):
    conn = Client(address=('127.0.0.1', 6000), authkey='secret password')
    print 'connection accepted'
    message = '+'
    for i in range(K):
        conn.send(message)
        answer = conn.recv()
    conn.close()


from multiprocessing.connection import Client
from multiprocessing import Process
import sys

print 'trying to connect'



N = int(sys.argv[1])
K = int(sys.argv[2])

for i in range(N):
    print 'starting process ', i
    p = Process(target=client, args=(K,))
    p.start()

    
