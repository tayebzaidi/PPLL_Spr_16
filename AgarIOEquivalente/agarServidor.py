#!/usr/bin/env python
import multiprocessing
from multiprocessing import Lock, Process, Manager
from multiprocessing.connection import Listener
from multiprocessing.connection import AuthenticationError
import json
import random


###Definir el formato de la lista 'estadoDeJuego'
#Hay un diccionario con todos los clientes
#Cada espacio en el diccionario tiene una lista con los coordinades

#Ser

def serve_client(conn, id, tablero, lock):
    process_name = multiprocessing.current_process().name
    
    conn.send(process_name) #Para identificacion
    
    while True:
        try:
            print tablero
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
            if m=='cerrando':
                break
            lock.acquire()
            tablero[m[0]] = m[1:]
            lock.release()
        except EOFError:
            print 'No recieve, connection abruptly closed by client'
            break
                
    conn.close()
    lock.acquire()
    del tablero[process_name]
    lock.release()
    print 'connection ', id, ' closed'
    
def governor(id, tablero, lock):
    process_name = multiprocessing.current_process().name
    desired_num_bolas = 20
    point_size = 10
    bola_idx = 0      
    
    while True:
        count_bolas=len(tablero)
        
        if count_bolas < desired_num_bolas:
            print count_bolas
            coord_x = random.randint(10,790)
            coord_y = random.randint(10,790)
            
            color = 
            
            updateTablero(tablero, lock, bola_idx, coord_x, coord_y, point_size, color)
            
            bola_idx += 1

    lock.acquire()
    del tablero[bola_idx]
    lock.release()
    print 'connection ', id, ' closed'
    
def updateTablero(tablero, lock, name, coord_x, coord_y, point_size, color):
    lock.acquire()
    tablero[name] = [(coord_x, coord_y), point_size, color]
    lock.release()

if __name__=="__main__":

    listener = Listener(address=('127.0.0.1', 6000))
    print("listener starting")
    
    lock = Lock()
    manager = Manager()    
    tablero=manager.dict()

    #Iniciar el proceso para los puntos aleatorios
    p=Process(target=governor, args=(listener.last_accepted,tablero, lock))
    p.start()
    
    print 'governor started'
    
    while True:
        print 'accepting conexions'
        try:
            conn = listener.accept()
            print 'connection accepted from', listener.last_accepted
            p = Process(target=serve_client, args=(conn, listener.last_accepted, tablero, lock))
            p.start()
            
            print p.name
            
            lock.acquire()
            tablero[p.name] = [200, 200, 20]
            lock.release()
            
            print tablero
        except AuthenticationError:
            print 'connection refused'
            
    listener.close()
    print 'end'
