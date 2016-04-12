# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 10:47:49 2016

@author: alumno
"""
from sys import version_info
if version_info.major == 2:
    # We are using Python 2.x
    import Tkinter as tk
elif version_info.major == 3:
    # We are using Python 3.x
    import tkinter as tk
from multiprocessing.connection import Client

#Custom imports
from agarTk import VentanaAgar
print 'trying to connect'


if __name__=="__main__":
    conn = Client(address=('127.0.0.1', 6000))
    print 'connection accepted'
    
    tablero = {}
    
    root = tk.Tk()
    VentanaAgar(root, tablero).pack(side="top", fill="both", expand=True)

    while True:
        print 'Esperando un mensaje'
        answer = conn.recv()
        print 'received message', answer
        
        
    conn.close()