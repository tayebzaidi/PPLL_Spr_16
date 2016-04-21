#!/usr/bin/env python
import multiprocessing
from multiprocessing import Lock, Process, Manager
from multiprocessing.connection import Listener
from multiprocessing.connection import AuthenticationError
import numpy
import json
import random
import time


###Definir el formato de la lista 'estadoDeJuego'
#Hay un diccionario con todos los clientes
#Cada espacio en el diccionario tiene una lista con los coordinades

#Ser

def serve_client(conn, ident, tableros, lock):
    nombre = conn.recv()
    
    if(nombre != ''):
        pass
    else:
        nombre='Anon'
    
    tablero_bolas = tableros[0]
    
    inertia_factor = float(30)
    
    print ident, type(ident)
    
    while True:
        try:
            print tableros
            tableros_send = [tab.copy() for tab in tableros]
            conn.send(tableros_send)
        except IOError:
            print 'No send, connection abruptly closed by client'
            break
        
        try:
            print 'waiting for message'
            m = conn.recv()
            print 'received message:', m, 'from', ident
            if m=='cerrando':
                break
            x_pos_raton = m[0]
            y_pos_raton = m[1]
            
            x_pos_bola = tablero_bolas[ident][0][0]
            y_pos_bola = tablero_bolas[ident][0][1]
            
            size = tablero_bolas[ident][1]
            
            x_dist = x_pos_raton - x_pos_bola
            y_dist = y_pos_raton - y_pos_bola
            
            mag = (x_dist**2 * y_dist**2)**(1/2)
            
            updated_pos_x = x_pos_bola + mag * x_dist / (inertia_factor)
            updated_pos_y = y_pos_bola + mag * y_dist / (inertia_factor)
            
            speed = ((updated_pos_x - x_pos_bola)**2 + (updated_pos_y - y_pos_bola)**2)**(1/2)
            max_speed = 100 / size
            
            if speed > max_speed:
                print 'at max speed'
                updated_pos_x = x_pos_bola + max_speed
            
            updateBola(tablero_bolas, lock, ident, updated_pos_x, updated_pos_y, size, '#FFFFFF', nombre)
        except EOFError:
            print 'No recieve, connection abruptly closed by client'
            break
                
    conn.close()
    lock.acquire()
    del tableros[0][ident]
    lock.release()
    print 'connection ', ident, ' closed'
    
def governor(id, tableros, lock):
    print 'Governor starting'
    desired_num_alimentos = 50
    desired_num_virus = 10
    alimento_point_size = 4
    virus_point_size = 15
    alimento_idx = 0     
    virus_idx = 0 
    
    _, tablero_alimentos, tablero_virus = tableros
    
    while True:
        count_alimentos=len(tablero_alimentos)
        count_virus = len(tablero_virus)
        
        if count_alimentos < desired_num_alimentos:
            print count_alimentos
            coord_x = random.randint(10,790)
            coord_y = random.randint(10,790)
            
            color = 'red'
            
            updateAlimento(tablero_alimentos, lock, alimento_idx, coord_x, coord_y, color)
            
            alimento_idx += 1

        if count_virus < desired_num_virus:
            print count_virus
            coord_x = random.randint(10, 790)
            coord_y = random.randint(10, 790)

            color = 'green'

            updateVirus(tablero_virus, lock, virus_idx, coord_x, coord_y, virus_point_size, color)
            virus_idx += 1
            
        time.sleep(random.random())

    conn.close()
    print 'connection ', id, ' closed'
    
def updateBola(tablero, lock, ident, coord_x, coord_y, point_size, color, nombre):
    lock.acquire()
    tablero[ident] = [(coord_x, coord_y), point_size, color, nombre]
    lock.release()
    
def updateAlimento(tablero, lock, ident, coord_x, coord_y,  color):
    lock.acquire()
    tablero[ident] = [(coord_x, coord_y), color]
    lock.release()
    
def updateVirus(tablero, lock, ident, coord_x, coord_y, point_size, color):
    lock.acquire()
    tablero[ident] = [(coord_x, coord_y), point_size, color]
    lock.release()

if __name__=="__main__":

    listener = Listener(address=('127.0.0.1', 6000))
    print("listener starting")
    
    lock = Lock()
    manager1 = Manager()  
    manager2 = Manager()
    manager3 = Manager()  
    tablero_alimentos=manager1.dict()
    tablero_virus=manager2.dict()
    tablero_bolas=manager3.dict()
    
    tableros = [tablero_bolas, tablero_alimentos, tablero_virus]

    #Iniciar el proceso para los puntos aleatorios y los viruses
    print "Starting Governor"
    
    p=Process(target=governor, args=(listener.last_accepted, tableros, lock))
    p.start()
    
    while True:
        print 'accepting conexions'
        try:
            conn = listener.accept()
            print 'connection accepted from', listener.last_accepted
            ident = listener.last_accepted[1]
            conn.send(listener.last_accepted)
            p = Process(target=serve_client, args=(conn, ident, tableros, lock))
            p.start()
            
            print p.name
            
            lock.acquire()
            tableros[0][ident] = [(200, 200), 20, '#FFFFFF', '']
            lock.release()
            
            print tableros
        except AuthenticationError:
            print 'connection refused'
            
    listener.close()
    print 'end'
