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

def serve_client(conn, id, tableros, lock):
    process_name = multiprocessing.current_process().name
    
    conn.send(process_name) #Para identificacion
    
    tablero_bolas = tableros[0]
    
    inertia_factor = float(30)
    
    while True:
        try:
            print tableros
            tableros_send = [tab.copy() for tab in tableros]
            table = json.dumps(tableros_send).encode('utf-8')
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
            x_pos_raton = m[0][0]
            y_pos_raton = m[0][1]
            
            x_pos_bola = tablero_bolas[process_name][0][0]
            y_pos_bola = tablero_bolas[process_name][0][1]
            
            x_dist = x_pos_raton - x_pos_bola
            y_dist = y_pos_raton - y_pos_bola
            
            mag = (x_dist**2 * y_dist**2)**(1/2)
            
            updated_pos_x = x_pos_bola + mag * x_dist / (inertia_factor)
            updated_pos_y = y_pos_bola + mag * y_dist / (inertia_factor)
            
            speed = ((updated_pos_x - x_pos_bola)**2 + (updated_pos_y - y_pos_bola)**2)**(1/2)
            max_speed = 100 / m[1]
            
            if speed > max_speed:
                print 'at max speed'
                updated_pos_x = x_pos_bola + max_speed
            
            updateTablero(tablero_bolas, lock, process_name, updated_pos_x, updated_pos_y, m[1], 'white')
        except EOFError:
            print 'No recieve, connection abruptly closed by client'
            break
                
    conn.close()
    lock.acquire()
    del tableros[0][process_name]
    lock.release()
    print 'connection ', id, ' closed'
    
def governor(id, tableros, lock):
    print 'Governor starting'
    process_name = multiprocessing.current_process().name
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
            
            updateTablero(tablero_alimentos, lock, alimento_idx, coord_x, coord_y, alimento_point_size, color)
            
            alimento_idx += 1

        if count_virus < desired_num_virus:
            print count_virus
            coord_x = random.randint(10, 790)
            coord_y = random.randint(10, 790)

            color = 'green'

            updateTablero(tablero_virus, lock, virus_idx, coord_x, coord_y, virus_point_size, color)
            virus_idx += 1
            
        time.sleep(random.random())

    conn.close()
    print 'connection ', id, ' closed'
    
def updateTablero(tablero, lock, name, coord_x, coord_y, point_size, color):
    lock.acquire()
    tablero[name] = [(coord_x, coord_y), point_size, color]
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
            p = Process(target=serve_client, args=(conn, listener.last_accepted, tableros, lock))
            p.start()
            
            print p.name
            
            lock.acquire()
            tableros[0][p.name] = [(200, 200), 20, 'white']
            lock.release()
            
            print tableros
        except AuthenticationError:
            print 'connection refused'
            
    listener.close()
    print 'end'
