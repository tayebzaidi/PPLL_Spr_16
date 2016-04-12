# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 11:29:57 2016

@author: alumno
"""

from multiprocessing import Process
from multiprocessing import Condition
from multiprocessing import current_process
from multiprocessing import Manager
from multiprocessing import Queue

import time, random

import Tkinter as tk

N = 20



    
class VentanaProductorConsumidor(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        self.frame = tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent   
        
        canvas = tk.Canvas(self.frame, width=600, height=200)
        canvas.pack()
        
        obj = []
        obj.append(canvas.create_oval(50, 150, 20, 120,fill="grey"))
        obj.append(canvas.create_oval(370, 150, 420, 120,fill="grey"))

        self.control = Condition()
        self.manager = Manager()
        self.queue = Queue()
        self.l = self.manager.list()
        print "almacen inicial", self.l[:]
        
        self.boton = tk.Button(self.frame, text="Iniciar procesos", command=self.BotonIniciar)
        self.boton.pack()
        self.updateQueue()                
        
    def updateQueue(self):
        if not self.queue.empty():
            item = self.queue.get()
            print item[:2]
            print item[2]
            
            if item[0][0] == 'p':
                obj[item[0][-1]]
           
        self.after(10, self.updateQueue)
        
        
    def BotonIniciar(self):
        self.productor = Process(target=self.p, name="productor1", args=(self.l,self.control,1))
        #self.productor2 = Process(target=self.p, name="productor2", args=(self.l,self.control,2))
        self.consumidor = Process(target=self.c, name="consumidor1", args=(self.l,self.control))
        #self.consumidor2 = Process(target=self.c, name="consumidor2", args=(self.l,self.control))        
        
        self.productor.start()
        self.productor2.start()
        
        self.consumidor.start()
        self.consumidor2.start()
            
        
    def p(self, almacen,control,i): 
        for v in range(N):
            #print current_process().name, "produciendo"
            self.queue.put([current_process().name, 'produciendo', almacen])
            time.sleep(random.random())
            control.acquire()
            while len(almacen) == 0:
                #print current_process().name, "esperando..."
                self.queue.put([current_process().name, 'esperando', almacen])
                control.wait()
            dato = str(i)+"."+str(v)+"+"		
            almacen.append(dato)
            self.queue.put([current_process().name, 'almacenando', almacen])
            #print current_process().name, "almacenando", dato
            time.sleep(random.random())
            control.notify_all()
            control.release()                 
    
    def c(self, almacen,control):
         for v in range(N):
            time.sleep(random.random())
            control.acquire()        
            while len(almacen) == 0:
                #print current_process().name, "esperando.."
                self.queue.put([current_process().name, 'esperando', almacen])
                control.wait()
            #print current_process().name, "desalmacenando"
            dato = almacen.pop(0)
            time.sleep(random.random())
            control.notify_all()
            control.release()
            self.queue.put([current_process().name, 'consumiendo', almacen])
            #print current_process().name, "consumiendo", dato[:-1]+"-"
                
if __name__ == "__main__":   
    
    root = tk.Tk()
    VentanaProductorConsumidor(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
    
    
