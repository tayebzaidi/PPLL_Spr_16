# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 10:47:49 2016

@author: alumno
"""

from multiprocessing.connection import Client
print 'trying to connect'
conn = Client(address=('147.96.18.19', 6000), authkey='secret password')
print 'connection accepted'
message = raw_input('Message to send? ')
print 'sending message'
conn.send(message)
print 'received message', conn.recv()
conn.close()