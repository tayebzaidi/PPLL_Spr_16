# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 10:47:49 2016

@author: alumno
"""

from multiprocessing.connection import Client
print 'trying to connect'

conn = Client(address=('127.0.0.1', 6000), authkey='secret password')
print 'connection accepted'

answer = ''
while answer != 'adios':
    message = raw_input('Message to send? ')
    print 'sending message'
    conn.send(message)
    answer = conn.recv()
    print 'received message', answer
    
conn.close()