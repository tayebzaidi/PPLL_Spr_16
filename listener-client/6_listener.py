# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 10:38:38 2016

@author: alumno
"""
from multiprocessing import Process
from multiprocessing.connection import Listener
from multiprocessing.connection import AuthenticationError
from multiprocessing import Lock, Manager
import multiprocessing

from time import time

def serve_client(conn, id, lock, usuarios):
    process_name = multiprocessing.current_process().name
    print process_name
    while True:
        try:
            m = conn.recv()
        except EOFError:
            print 'No recieve, connection abruptly closed by client'
            break
        
        if m != 'cierra':
            print 'received message:', m, 'from', id
            answer = 'ok'
        else:
            answer = 'cerrando'
            
        try:
            conn.send(answer)
        except IOError:
            print 'No send, connection abruptly closed by client'
            break
        
    conn.close()
    lock.acquire()
    del usuarios[process_name]
    lock.release()
    print 'connection ', id, ' closed'


if __name__=="__main__":
    
    listener = Listener(address=('127.0.0.1', 6000), authkey='secret password')
    print 'listener starting'
    
    lock = Lock()
    manager = Manager()
    usuarios = manager.dict()
    
    while True:
        print 'accepting conexions'
        try:
            conn = listener.accept()
            print 'connection accepted from', listener.last_accepted
            p = Process(target=serve_client, args=(conn, listener.last_accepted, lock, usuarios))
            p.start()
            
            print p.name
            
            lock.acquire()
            usuarios[p.name] = listener.last_accepted
            lock.release()
            
            print usuarios
        except AuthenticationError:
            print 'connection refused'
            
    listener.close()
    print 'end'
