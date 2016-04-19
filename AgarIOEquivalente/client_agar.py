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
    def __init__(self, parent, tableros,*args, **kwargs):
        self.tableros = tableros
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
        print 'Esperando identificacion'
        self.my_name = self.conn.recv()
        self.updateEstado() 

    def updateEstado(self):
        print 'Esperando un mensaje'
        newTableros = self.conn.recv()
        print newTableros
        self.tableros = json.loads(newTableros.decode('utf-8'))
        print 'received message', newTableros
        self.canvas.delete('all')
        for tablero in self.tableros:
            for key, val in tablero.iteritems():
                print val
                x = val[0][0]
                y = val[0][1]
                r = val[1]
                color = val[2]
                print x,y,r
                self.canvas.create_oval(x-r, y-r, x+r, y+r,fill=color)
        self.conn.send([(self.mouse_x, self.mouse_y), 20])
        self.after(10, self.updateEstado)
            
    def updateTablero(self, event):
        self.mouse_x = event.x
        self.mouse_y = event.y

        #(x,y), r, color = self.tablero[self.my_name]

        #self.x_y_vec = (self.mouse_x - x, self.mouse_y - y)
        
    def cerrarJuego(self):
        print 'mandando mensaje de cerrar'
        self.conn.send('cerrando')
        sys.exit()
        
            
        
        

if __name__=="__main__":
    
    
    tableros = [{},{},{}]
    
    root = tk.Tk()
    VentanaAgar(root, tableros).pack(side="top", fill="both", expand=True)
    root.mainloop()
