#!/usr/bin/env python

from multiprocessing import Lock, Process, Manager
from multiprocessing.connection import Listener
from multiprocessing.connection import AuthenticationError

#Importes locales
from agarTk import VentanaAgar

###Definir el formato de la lista 'estadoDeJuego'
#Hay un matrice con las posiciones

#Ser

def serve_client(conn, id, usuarios, count):
    pass

if __name__=="__main__":

    listener = Listener(address=(127.0.0.1, 6000))
    print("listener starting")
    
    lock = Lock()
    manager = Manager()    
    estadoDeJuego=manager.list()

    root = tk.Tk()
    VentanaAgar(root, estadoDeJuego).pack(side="top", fill="both", expand=True)
    root.mainloop()
