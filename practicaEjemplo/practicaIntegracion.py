# -*- coding: utf-8 -*-
"""
Created on Tue May 17 12:09:08 2016

@author: alumno
"""
from mrjob.job import MRJob
from mrjob.step import MRStep
from mrjob.compat import jobconf_from_env
import string
import time
import re

regex = '(.*?) - - \[(.*?)\] "(.*?)" (\d+)'
#Time pattern
pattern = '%d/%b/%Y:%H:%M:%S'
T = 1800 #30 minutes in seconds

class MRLog_Info(MRJob):
    #SORT_VALUES = True

    def mapper(self, _, line):
        data = re.match(regex, line).groups()
        usuario = data[0]
        date = data[1]
        webpage = data[2]
        date_time = date[:20]
        epoch = time.mktime(time.strptime(date_time, pattern))
        yield usuario, (epoch, webpage)
            
    def reducer(self, usuario, data):
        session_count = 0 #Offset for first
        comportamientos = {}
        time_prev = -10000 #Before epoch para que tengamos el principio
        for tiempo, webpage in data:
            session_prev = session_count
            if tiempo - time_prev > T:
                session_count += 1
                comportamientos['comportamiento'+str(session_count)] = set()
            time_prev = tiempo
            comportamientos['comportamiento'+str(session_count)].add(webpage)
            if session_count - session_prev > 0:
                for key, val in comportamientos.iteritems():
                    comportamiento = sorted(list(val))
                    comportamientos[key] = comportamiento
                    yield comportamiento, (usuario, session_count, comportamientos)
        
    def compara(self, comportamiento, data):
        usuario_list = set()
        for usuario, session_count, comportamientos in data:
            usuario_list.add(usuario)
            
            pass
        yield usuario, (comportamiento, usuario_list)
        
    def agregar(self, usuario, data):
        pass
            
            
    def steps(self):
        return [
            MRStep(mapper = self.mapper,
                    reducer = self.reducer),
            MRStep(reducer = self.compara),
            MRStep(reducer = self.agregar)
        ]
        
if __name__ == '__main__':
    MRLog_Info.run()