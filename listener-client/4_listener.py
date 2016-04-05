# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 10:38:38 2016

@author: alumno
"""

from multiprocessing.connection import Listener
from multiprocessing.connection import AuthenticationError

listener = Listener(address=('127.0.0.1', 6000), authkey='secret password')
print 'listener starting'

open_conn = False 
while True:
    while not open_conn:
        try:
            conn = listener.accept()
            print 'connection accepted from', listener.last_accepted
            open_conn = True
        except AuthenticationError:
            print 'connection refused'

    while open_conn:
        m = conn.recv()
        print 'received message:', m
        if m == 'hola':
            answer = 'adios'
            open_conn = False
        else:
            answer = 'ok'
        conn.send(answer)
        
    conn.close()
    print 'connection closed'
listener.close()