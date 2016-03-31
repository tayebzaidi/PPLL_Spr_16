# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 10:38:38 2016

@author: alumno
"""

from multiprocessing.connection import Listener

listener = Listener(address=('127.0.0.1', 6000), authkey='secret password')
print 'listener starting'
conn = listener.accept()
print 'connection accepted from', listener.last_accepted
m = conn.recv()
print 'received message:', m
conn.send('ok')
conn.close()
print 'connection closed'
listener.close()