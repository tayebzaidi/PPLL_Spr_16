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
    def __init__(self, parent, *args, **kwargs):
        self.tableros = [{},{},{}]
        self.alimento_sz = 4
        self.virus_sz = 15
        self.mouse_x = 50
        self.mouse_y = 50
        
        self.frame = tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.canvas = tk.Canvas(self.frame, width=1200, height=800)
        self.canvas.pack()
        
        self.boton_iniciar = tk.Button(self.frame, text="Iniciar juego", command=self.iniciarJuego)
        self.boton_iniciar.pack()
        self.boton_cerrar = tk.Button(self.frame, text="Cerrar juego", command=self.cerrarJuego)
        self.boton_cerrar.pack()
        
        self.canvas.bind('<Motion>', self.updateTablero)
        
    def iniciarJuego(self):

        self.t = tk.Toplevel(self)
        self.t.wm_title("Entrar tu nombre")

        self.submit = tk.Button(self.t, text="Submit", command= lambda: self.termIniciar(self.E1.get()))
        self.submit.pack()       
        
        self.l = tk.Label(self.t, text="This is window")
        self.l.pack()

        self.E1 = tk.Entry(self.t, bd=5)
        self.E1.pack()        
        print self.E1.get()
        
        
    def termIniciar(self, nombre):
        self.t.destroy()        
        
        self.conn = Client(address=('147.96.18.196', 6000), authkey = 'secret password')
        print 'connection accepted'
        
        #print 'Esperando identificacion'        
        #(_, self.my_name) = self.conn.recv()
        
        self.conn.send(nombre)

        self.updateEstado() 

    def updateEstado(self):
        print 'Esperando un mensaje'
        newTableros = self.conn.recv()
        print 'message received'
        self.tableros = newTableros[1:]
        #print 'received message', newTableros
        self.my_name = newTableros[0]
        self.canvas.delete('all')
        for key, val in self.tableros[0].iteritems():
            x = val[0][0]
            y = val[0][1]
            r = val[1]
            color = val[2]
            nombre = val[3]
            self.canvas.create_oval(x-r, y-r, x+r, y+r,fill=color)
            self.canvas.create_text(x,y,text=nombre)
        for key, val in self.tableros[1].iteritems():
            x = val[0][0]
            y = val[0][1] 
            color = val[1]
            self.canvas.create_oval(x-self.alimento_sz, y-self.alimento_sz, x+self.alimento_sz, y+self.alimento_sz,fill=color)
            
        for key, val in self.tableros[2].iteritems():
            x = val[0][0]
            y = val[0][1]
            color = val[1]
            self.canvas.create_oval(x-self.virus_sz, y-self.virus_sz, x+self.virus_sz, y+self.virus_sz,fill=color)
        self.conn.send([self.mouse_x, self.mouse_y])
        self.after(5, self.updateEstado)
            
    def updateTablero(self, event):
        self.mouse_x = event.x
        self.mouse_y = event.y

        #(x,y), r, color = self.tablero[self.my_name]

        #self.x_y_vec = (self.mouse_x - x, self.mouse_y - y)
        
    def cerrarJuego(self):
        
        sys.exit()
        
            
        
        

if __name__=="__main__":
    
    root = tk.Tk()
    VentanaAgar(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
