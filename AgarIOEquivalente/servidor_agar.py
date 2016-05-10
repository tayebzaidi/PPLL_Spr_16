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
def norm(x, y):
    return math.sqrt(x**2 + y**2)

def randcolor():
    r1 = random.randint(0,255)
    r2 = random.randint(0,255)
    r3 = random.randint(0,255)
    color_string = '#%02X%02X%02X' % (r1,r2,r3)
    return color_string
    
def trasladarCoordinadas(tableros, ident, alcance_ventana_x, alcance_ventana_y):
    
    x_pos_bola = tableros[1][ident][0][0]
    y_pos_bola = tableros[1][ident][0][1]

    temp_tableros = tableros[1:]
    tableros_send = [{},{},{}]
    for i in range(len(temp_tableros)):
                for key, val in temp_tableros[i].items():
                    coord_x = val[0][0]
                    coord_y = val[0][1]
                    
                    new_coord_x = coord_x - x_pos_bola + alcance_ventana_x / 2
                    new_coord_y = coord_y - y_pos_bola + alcance_ventana_y / 2
                    
                    if i == 0:
                        temp_radius_bola = val[1]
                        temp_color_bola = val[2]
                        temp_nombre_bola = val[3]
                        tableros_send[1][key] = [(new_coord_x, new_coord_y), temp_radius_bola, temp_color_bola, temp_nombre_bola]
                    if i == 1:
                        temp_color_alimento = val[1]
                        tableros_send[2][key] = [(new_coord_x, new_coord_y), temp_color_alimento]
                    if i == 2:
                        temp_color_virus = val[1]
                        tableros_send[3][key] = [(new_coord_x, new_coord_y), temp_color_virus]
    
    return tableros_send

def serve_client(conn, ident, tableros, lock):
    alcance_ventana_x = 1200
    alcance_ventana_y = 800
    color_bola = randcolor()
    game_sz_limit_x = 2000
    game_sz_limit_y = 2000
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
            
            #Coordinate shifting justo antes de mandarlos
            tableros_send = trasladarCoordinadas(tableros_send, ident, alcance_ventana_x, alcance_ventana_y)
            
            conn.send(tableros_send)
        except Exception, e:
            print str(e)
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
            
            def speed(mass):
                velocidad = 4 - mass * 0.001
                if velocidad < 2.5:
                    velocid = 2.5
                return velocidad
            
            x_pos_raton = temp_x_pos_raton - 600
            y_pos_raton = temp_y_pos_raton - 400 
            
            raton_pos = [x_pos_raton, y_pos_raton]
            
            x_pos_bola = tablero_bolas[ident][0][0]
            y_pos_bola = tablero_bolas[ident][0][1]
            
            radius_bola = tablero_bolas[ident][1]
            mass_bola = radius_bola**2 * math.pi
            
            if abs(x_pos_raton) < 5 and abs(x_pos_raton) < 5:
                velocidad = 0
            else:
                velocidad = speed(mass_bola)
            mag = norm(raton_pos[0], raton_pos[1])
            if mag == 0:
                print 'mag is zero'
                mag  = 1
            x_pos_bola += velocidad * x_pos_raton / mag 
            y_pos_bola += velocidad * y_pos_raton / mag
            
            bola_pos = np.array([x_pos_bola, y_pos_bola])
            
            speed = ((x_pos_bola - x_pos_bola)**2 + (y_pos_bola - y_pos_bola)**2)**(1/2)
            
            time.sleep(0.01)
            #if speed > max_speed:
            #    print 'at max speed'
            #    x_pos_bola = x_pos_bola + max_speed
            
            updateBola(tablero_bolas, lock, ident, x_pos_bola, y_pos_bola, radius_bola, color_bola, nombre)
        except Exception, e:
            print str(e)
            print 'No recieve, connection abruptly closed by client'
            break
        
        #Probar para ver si ha comido o ha sido comido
    
        try:
            
            def alcance_de_bola(r1, r2):
                alcance = r1/3 + r2/3
                return alcance
                
            for key, val in tablero_bolas.items():
                otra_bola_x = val[0][0]
                otra_bola_y = val[0][1]
                mass_otra_bola = val[1]**2 * math.pi
                alcance_bola = alcance_de_bola(val[1], radius_bola)
                #Still need to implement range
                if (otra_bola_x - alcance_bola <= x_pos_bola <= otra_bola_x + alcance_bola and 
                    otra_bola_y - alcance_bola <= y_pos_bola <= otra_bola_y + alcance_bola and key != ident):
                    if mass_otra_bola > mass_bola:
                        deleteEntry(tablero_bolas, lock, ident)
                        new_mass = mass_otra_bola + mass_bola
                        radius_otra_bola = math.sqrt(new_mass / math.pi)
                        otra_color = val[2]
                        otra_nombre = val[3]
                        updateBola(tablero_bolas, lock, key, otra_bola_x, otra_bola_y, radius_otra_bola, otra_color, otra_nombre)
                    elif mass_otra_bola < mass_bola:
                        deleteEntry(tablero_bolas, lock, key)
                        new_mass = mass_otra_bola + mass_bola
                        radius_bola = math.sqrt(new_mass / math.pi)
                        updateBola(tablero_bolas, lock, ident, x_pos_bola, y_pos_bola, radius_bola, color_bola, nombre)
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
                    radius_bola = math.sqrt(new_mass / math.pi)
                    deleteEntry(tablero_alimentos, lock, key)
                    updateBola(tablero_bolas, lock, ident, x_pos_bola, y_pos_bola, radius_bola, color_bola, nombre)
                    
            #Border check
            if x_pos_bola <= 0:
                x_pos_bola = 0
            elif x_pos_bola >= window_limit_x:
                x_pos_bola = window_limit_x
                
            if y_pos_bola <= 0:
                y_pos_bola = 0
            elif y_pos_bola >= window_limit_y:
                y_pos_bola = window_limit_y
                
            updateBola(tablero_bolas, lock, ident, x_pos_bola, y_pos_bola, radius_bola, color_bola, nombre)
                            
        except Exception, e:
            print str(e)
            print 'Fatal error occurred in eating calculations'
            break                        
    
    print 'spectating now'
        
    while True:
        try:
            randkey
        except Exception, e:
            randkey = random.choice(tablero_bolas.keys())
            print 'getting new key'
            print randkey
            print str(e)
        
        try:
            randkey
        except Exception, e:
            print "error not recoverable, can't find randkey"
            print str(e)
            break
            
        try:
            yo = ident
            tableros_send = [yo, tablero_bolas.copy(), tablero_alimentos.copy(), tablero_virus.copy()]
            
            x_pos_bola = tablero_bolas[randkey][0][0]
            y_pos_bola = tablero_bolas[randkey][0][1]
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
                        temp_color_virus = val[1]
                        tableros_send[3][key] = [(new_coord_x, new_coord_y), temp_color_virus]
            #print 'sending tablero to ', randkey  
            conn.send(tableros_send)
        
        except Exception, e:
            print str(e)
            print 'spectating failed, trying with new entry'
            break
            
        try:
            #print 'waiting for message'
            m = conn.recv()
        except Exception, e:
            print str(e)
            print 'spectating failed on receive end'
            
    try:
        test = tablero_bolas[ident]
        deleteEntry(tablero_bolas, lock, ident)
    except:
        print 'already deleted'
    print 'connection ', ident, ' closed'
    
def governor(id, tableros, lock):
    print 'Governor starting'
    desired_num_alimentos = 100
    desired_num_virus = 30
    alimento_point_size = 2

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

            updateVirus(tablero_virus, lock, virus_idx, coord_x, coord_y, color)
            virus_idx += 1
            
        time.sleep(random.random() / 50)

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
    
def updateVirus(tablero, lock, ident, coord_x, coord_y, color):
    lock.acquire()
    tablero[ident] = [(coord_x, coord_y),  color]
    lock.release()
    
def deleteEntry(tablero, lock, ident):
    lock.acquire()
    del tablero[ident]
    lock.release()

if __name__=="__main__":

    listener = Listener(address=('127.0.0.1', 6000), authkey='secret password')
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
