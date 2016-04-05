# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 10:47:49 2016

@author: alumno
"""

from multiprocessing.connection import Client
print 'trying to connect'

conn = Client(address=('127.0.0.1', 6000), authkey='secret password')
print 'connection accepted'

#no respeta el protocolo y sin recibir 'adios' o sin esperar
message = raw_input('Message to send? (q -> quit no send, n -> send but no wait for answer) ')
if message != 'q':    
    print 'sending message'
    conn.send(message)
    if message != 'n':
        answer = conn.recv()
        print 'received message', answer
print 'made it'
conn.close()