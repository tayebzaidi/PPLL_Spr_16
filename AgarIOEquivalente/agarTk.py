#!/usr/bin/env python

from sys import version_info
if version_info.major == 2:
    # We are using Python 2.x
    import Tkinter as tk
elif version_info.major == 3:
    # We are using Python 3.x
    import tkinter as tk
from multiprocessing.connection import Client
from multiprocessing import Queue

#Custom imports
print 'trying to connect'

class VentanaAgar(tk.Frame):
    def __init__(self, parent, tablero, conn, *args, **kwargs):
        self.tablero = tablero
        self.conn = conn
        
        self.frame = tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.canvas = tk.Canvas(self.frame, width=800, height=800)
        self.canvas.pack()
        
        self.boton = tk.Button(self.frame, text="Iniciar juego")
        self.boton.pack()
        
        self.frame.bind('<Motion>', self.updateTablero)
        
        self.updateEstado() #Utilizar la cola para seguir

    def updateEstado(self):
        print 'Esperando un mensaje'
        newTablero = conn.recv()
        self.tablero = newTablero
        print 'received message', newTablero
        for key, val in self.tablero:
            x = val[1]
            y = val[2]
            r = val[3]
            self.canvas.create_oval(x-r, y-r, x+r, y+r,fill="white")
            
    def updateTablero(self, event):
        pass
            
        
        

if __name__=="__main__":
    conn = Client(address=('127.0.0.1', 6000))
    print 'connection accepted'
    
    tablero = {}
    
    root = tk.Tk()
    VentanaAgar(root, tablero, conn).pack(side="top", fill="both", expand=True)

    while True:
        print 'Esperando un mensaje'
        answer = conn.recv()
        print 'received message', answer
        
        print 'sending message'
        conn.send(message)