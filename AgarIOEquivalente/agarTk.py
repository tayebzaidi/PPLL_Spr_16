#!/usr/bin/env python

from sys import version_info
if version_info.major == 2:
    # We are using Python 2.x
    import Tkinter as tk
elif version_info.major == 3:
    # We are using Python 3.x
    import tkinter as tk
from multiprocessing.connection import Client
import json
import sys

#Custom imports
print 'trying to connect'

class VentanaAgar(tk.Frame):
    def __init__(self, parent, tablero,*args, **kwargs):
        self.tablero = tablero
        self.mouse_x = 50
        self.mouse_y = 50
        
        self.frame = tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.canvas = tk.Canvas(self.frame, width=800, height=800)
        self.canvas.pack()
        
        self.boton_iniciar = tk.Button(self.frame, text="Iniciar juego", command=self.iniciarJuego)
        self.boton_iniciar.pack()
        self.boton_cerrar = tk.Button(self.frame, text="Cerrar juego", command=self.cerrarJuego)
        self.boton_cerrar.pack()
        
        self.canvas.bind('<Motion>', self.updateTablero)
        
    def iniciarJuego(self):
        self.conn = Client(address=('127.0.0.1', 6000))
        print 'connection accepted'
        self.updateEstado() #Utilizar la cola para seguir

    def updateEstado(self):
        print 'Esperando un mensaje'
        newTablero = self.conn.recv()
        print newTablero
        self.tablero = json.loads(newTablero.decode('utf-8'))
        self.my_name = self.tablero['me']
        print 'received message', newTablero
        self.canvas.delete('all')
        for key, val in self.tablero.iteritems():
            if key != 'me':
                x = val[0]
                y = val[1]
                r = val[2]
                print x,y,r
                self.canvas.create_oval(x-r, y-r, x+r, y+r,fill="white")
        self.conn.send([self.my_name, self.mouse_x, self.mouse_y, 20])
        self.after(10, self.updateEstado)
            
    def updateTablero(self, event):
        self.mouse_x = event.x
        self.mouse_y = event.y
        
    def cerrarJuego(self):
        print 'mandando mensaje de cerrar'
        self.conn.send('cerrando')
        a = self.conn.recv()
        print a
        sys.exit()
        
            
        
        

if __name__=="__main__":
    
    
    tablero = {}
    
    root = tk.Tk()
    VentanaAgar(root, tablero).pack(side="top", fill="both", expand=True)
    root.mainloop()

    while True:
        print 'Esperando un mensaje'
        answer = conn.recv()
        print 'received message', answer
        
        print 'sending message'
        conn.send(message)
