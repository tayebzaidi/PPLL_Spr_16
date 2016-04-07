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

def serve_client(conn, id, lock, usuarios, count):
    process_name = multiprocessing.current_process().name
    print count
    print usuarios
    print process_name
    while True:
        try:
            m = conn.recv()
            lock.acquire()
            count[1] += 1
            lock.release()
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
        
        print count[1]
        
    conn.close()
    lock.acquire()
    del usuarios[process_name]
    count[0] -= 1
    lock.release()
    print 'connection ', id, ' closed'
    print usuarios
    print count


if __name__=="__main__":
    
    listener = Listener(address=('127.0.0.1', 6000), authkey='secret password')
    print 'listener starting'
    
    lock = Lock()
    manager = Manager()
    usuarios = manager.dict()
    count = manager.list()
    count.append(0)
    count.append(0)
    count[0] = 0
    count[1] = 0

    
    while True:
        print 'accepting conexions'
        try:
            conn = listener.accept()
            print 'connection accepted from', listener.last_accepted
            p = Process(target=serve_client, args=(conn, listener.last_accepted, lock, usuarios, count))
            p.start()
            
            print p.name
            
            lock.acquire()
            usuarios[p.name] = listener.last_accepted
            count[0] += 1
            lock.release()
            
            print usuarios
            print count
        except AuthenticationError:
            print 'connection refused'
            
    listener.close()
    print 'end'
