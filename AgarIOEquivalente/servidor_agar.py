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

def randcolor():
    r1 = random.randint(0,255)
    r2 = random.randint(0,255)
    r3 = random.randint(0,255)
    color_string = '#%02X%02X%02X' % (r1,r2,r3)
    return color_string

def serve_client(conn, ident, tableros, lock):

    color_bola = randcolor()
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
            yo = ident
            tableros_send = [yo, tablero_bolas.copy(), tablero_alimentos.copy(), tablero_virus.copy()]
            
            x_pos_bola = tablero_bolas[ident][0][0]
            y_pos_bola = tablero_bolas[ident][0][1]
            #Coordinate shifting justo antes de mandarlos
            temp_tableros = tableros_send[1:]
            for i in range(len(temp_tableros)):
                for key, val in temp_tableros[i].items():
                    coord_x = val[0][0]
                    coord_y = val[0][1]
                    
                    
                    new_coord_x = coord_x - x_pos_bola + 600
                    new_coord_y = coord_y - y_pos_bola + 400
                    
                    if i == 0:
                        temp_radius_bola = val[1]
                        temp_color_bola = val[2]
                        temp_nombre_bola = val[3]
                        tableros_send[1][key] = [(new_coord_x, new_coord_y), temp_radius_bola, temp_color_bola, temp_nombre_bola]
                    if i == 1:
                        temp_color_alimento = val[1]
                        tableros_send[2][key] = [(new_coord_x, new_coord_y), temp_color_alimento]
                    if i == 2:
                        temp_radius_virus = val[1]
                        temp_color_virus = val[2]
                        tableros_send[3][key] = [(new_coord_x, new_coord_y), temp_radius_virus, temp_color_virus]  
   
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
            temp_x_pos_raton = m[0]
            temp_y_pos_raton = m[1]
            
            x_pos_raton = temp_x_pos_raton - 600 + x_pos_bola
            y_pos_raton = temp_y_pos_raton - 400 + y_pos_bola
            
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
            
            updateBola(tablero_bolas, lock, ident, updated_pos_x, updated_pos_y, radius_bola, color_bola, nombre)
        except:
            print 'No recieve, connection abruptly closed by client'
            break
        
        #Probar para ver si ha comido o ha sido comido
    
        try:
            alcance_ventana_x = 1100 / 2
            alcance_ventana_y = 1500 / 2
            def alcance_de_bola(r1, r2):
                alcance = r1/3 + r2/3
                return alcance
                
            for key, val in tablero_bolas.items():
                otra_bola_x = val[0][0]
                otra_bola_y = val[0][1]
                mass_otra_bola = val[1]**2 * math.pi
                alcance_bola = alcance_de_bola(val[1], radius_bola)
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
                        updateBola(tablero_bolas, lock, ident, updated_pos_x, updated_pos_y, new_radius, color_bola, nombre)
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
                    updateBola(tablero_bolas, lock, ident, updated_pos_x, updated_pos_y, new_radius, color_bola, nombre)
        except:
            print 'Fatal error occurred in eating calculations'
            break                        
        
        #Coordinate shifting
        
        
                    
                    
    
    deleteEntry(tablero_bolas, lock, ident)                    
    conn.close()
    print 'connection ', ident, ' closed'
    
def governor(id, tableros, lock):
    print 'Governor starting'
    desired_num_alimentos = 100
    desired_num_virus = 30
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
            coord_x = random.randint(10,1990)
            coord_y = random.randint(10,1990)
            
            color = randcolor()
            
            updateAlimento(tablero_alimentos, lock, alimento_idx, coord_x, coord_y, color)
            
            alimento_idx += 1

        if count_virus < desired_num_virus:
            #print count_virus
            coord_x = random.randint(10, 1990)
            coord_y = random.randint(10, 1990)

            color = 'green'

            updateVirus(tablero_virus, lock, virus_idx, coord_x, coord_y, virus_point_size, color)
            virus_idx += 1
            
        time.sleep(random.random() / 100)

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
            #conn.send(listener.last_accepted)
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
