#!/usr/bin/env python
import multiprocessing
from multiprocessing import Lock, Process, Manager
from multiprocessing.connection import Listener
from multiprocessing.connection import AuthenticationError
import numpy as np
import math
import json
import random
import time


###Definir el formato de la lista 'estadoDeJuego'
#Hay un diccionario con todos los clientes
#Cada espacio en el diccionario tiene una lista con los coordinades

#Ser

def serve_client(conn, ident, tableros, lock):

    color = '#FFFFFF'
    alimento_point_size = 2
    mass_alimento = alimento_point_size ** 2 * math.pi
    nombre = conn.recv()
    
    if(nombre != ''):
        pass
    else:
        nombre='Anon'
    
    tablero_bolas = tableros[0]
    tablero_alimentos = tableros[1]
    tablero_virus = tableros[2]
    
    inertia_factor = float(30)
    
    
    while True:
        try:
            tableros_send = [tab.copy() for tab in tableros]
            conn.send(tableros_send)
        except IOError:
            print 'No send, connection abruptly closed by client'
            break
        
       
            
        try:
            #print 'waiting for message'
            m = conn.recv()
            #print 'received message:', m, 'from', ident
            #if m=='cerrando':
            #    break
            x_pos_raton = m[0]
            y_pos_raton = m[1]
            
            x_pos_bola = tablero_bolas[ident][0][0]
            y_pos_bola = tablero_bolas[ident][0][1]
            
            radius_bola = tablero_bolas[ident][1]
            mass_bola = radius_bola**2 * math.pi
            
            x_dist = x_pos_raton - x_pos_bola
            y_dist = y_pos_raton - y_pos_bola
            
            mag = (x_dist**2 * y_dist**2)**(1/2)
            
            updated_pos_x = x_pos_bola + mag * x_dist / (inertia_factor)
            updated_pos_y = y_pos_bola + mag * y_dist / (inertia_factor)
            
            bola_pos = np.array([updated_pos_x, updated_pos_y])
            
            speed = ((updated_pos_x - x_pos_bola)**2 + (updated_pos_y - y_pos_bola)**2)**(1/2)
            
            
            #if speed > max_speed:
            #    print 'at max speed'
            #    updated_pos_x = x_pos_bola + max_speed
            
            updateBola(tablero_bolas, lock, ident, updated_pos_x, updated_pos_y, radius_bola, '#FFFFFF', nombre)
        except:
            print 'No recieve, connection abruptly closed by client'
            break
            
        #Probar para ver si ha comido o ha sido comido
    
        try:
            alcance_bola = 10
            def alcance_de_bola(m1, m2):
                pass
            for key, val in tablero_bolas.items():
                otra_bola_x = val[0][0]
                otra_bola_y = val[0][1]
                mass_otra_bola = val[1]**2 * math.pi
                #Still need to implement range
                if (otra_bola_x - alcance_bola <= updated_pos_x <= otra_bola_x + alcance_bola and 
                    otra_bola_y - alcance_bola <= updated_pos_y <= otra_bola_y + alcance_bola and key != ident):
                    if mass_otra_bola > mass_bola:
                        deleteEntry(tablero_bolas, lock, ident)
                        new_mass = mass_otra_bola + mass_bola
                        new_radius = math.sqrt(new_mass / math.pi)
                        otra_color = val[2]
                        otra_nombre = val[3]
                        updateBola(tablero_bolas, lock, key, otra_bola_x, otra_bola_y, new_radius, otra_color, otra_nombre)
                    elif mass_otra_bola < mass_bola:
                        deleteEntry(tablero_bolas, lock, key)
                        new_mass = mass_otra_bola + mass_bola
                        new_radius = math.sqrt(new_mass / math.pi)
                        updateBola(tablero_bolas, lock, ident, updated_pos_x, updated_pos_y, new_radius, color, nombre)
                    else:
                        pass
            for key, val in tablero_alimentos.items():
                alimento_x = val[0][0]
                alimento_y = val[0][1]
                alimento_pos = np.array([val[0][0], val[0][1]])
                #Hay que tener una manera para determinar el alcance
                dist = np.linalg.norm(alimento_pos - bola_pos) #Un circulo centrado en la bola (alcance)
                if dist <= radius_bola + alimento_point_size:
                    print 'alimento about to be eaten'
                    new_mass = mass_bola + mass_alimento
                    new_radius = math.sqrt(new_mass / math.pi)
                    deleteEntry(tablero_alimentos, lock, key)
                    updateBola(tablero_bolas, lock, ident, updated_pos_x, updated_pos_y, new_radius, color, nombre)
        except:
            print 'Fatal error occurred in eating calculations'
            break                        
    
    deleteEntry(tablero_bolas, lock, ident)                    
    conn.close()
    print 'connection ', ident, ' closed'
    
def governor(id, tableros, lock):
    print 'Governor starting'
    desired_num_alimentos = 50
    desired_num_virus = 10
    alimento_point_size = 2
    virus_point_size = 15
    alimento_idx = 0     
    virus_idx = 0 
    
    _, tablero_alimentos, tablero_virus = tableros
    
    while True:
        count_alimentos=len(tablero_alimentos)
        count_virus = len(tablero_virus)
        
        if count_alimentos < desired_num_alimentos:
            #print count_alimentos
            coord_x = random.randint(10,790)
            coord_y = random.randint(10,790)
            
            color = 'red'
            
            updateAlimento(tablero_alimentos, lock, alimento_idx, coord_x, coord_y, color)
            
            alimento_idx += 1

        if count_virus < desired_num_virus:
            #print count_virus
            coord_x = random.randint(10, 790)
            coord_y = random.randint(10, 790)

            color = 'green'

            updateVirus(tablero_virus, lock, virus_idx, coord_x, coord_y, virus_point_size, color)
            virus_idx += 1
            
        time.sleep(random.random() / 10)

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
    
def deleteEntry(tablero, lock, ident):
    lock.acquire()
    del tablero[ident]
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
            tableros[0][ident] = [(200, 200), 5, '#FFFFFF', '']
            lock.release()
            
            print tableros
        except AuthenticationError:
            print 'connection refused'
            
    listener.close()
    print 'end'
