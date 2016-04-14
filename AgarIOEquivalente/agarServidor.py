#!/usr/bin/env python
import multiprocessing
from multiprocessing import Lock, Process, Manager
from multiprocessing.connection import Listener
from multiprocessing.connection import AuthenticationError
import json


###Definir el formato de la lista 'estadoDeJuego'
#Hay un diccionario con todos los clientes
#Cada espacio en el diccionario tiene una lista con los coordinades

#Ser

def serve_client(conn, id, tablero, usuarios, lock):
    process_name = multiprocessing.current_process().name
    print tablero
    
    while True:
        try:
            lock.acquire()
            tablero['me'] = process_name
            lock.release()
            tablero_send = tablero.copy()
            table = json.dumps(tablero_send).encode('utf-8')
            conn.send(table)
        except IOError:
            print 'No send, connection abruptly closed by client'
            break
        
        try:
            print 'waiting for message'
            m = conn.recv()
            print 'received message:', m, 'from', id
            lock.acquire()
            tablero[m[0]] = m[1:]
            lock.release()
        except EOFError:
            print 'No recieve, connection abruptly closed by client'
            break
                
    conn.close()
    lock.acquire()
    del usuarios[process_name]
    del tablero[process_name]
    lock.release()
    print 'connection ', id, ' closed'
    print usuarios
    
        

if __name__=="__main__":

    listener = Listener(address=('127.0.0.1', 6000))
    print("listener starting")
    
    lock = Lock()
    manager = Manager()    
    tablero=manager.dict()
    usuarios=manager.dict()
    
    while True:
        print 'accepting conexions'
        try:
            conn = listener.accept()
            print 'connection accepted from', listener.last_accepted
            p = Process(target=serve_client, args=(conn, listener.last_accepted, tablero, usuarios, lock))
            p.start()
            
            print p.name
            
            lock.acquire()
            usuarios[p.name] = listener.last_accepted
            tablero[p.name] = [p.name, 200, 200, 20]
            lock.release()
            
            print tablero
        except AuthenticationError:
            print 'connection refused'
            
    listener.close()
    print 'end'
