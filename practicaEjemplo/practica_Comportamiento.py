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
T = 1800 #30 minutos en segundos

class MRLog_Info(MRJob):
    #SORT_VALUES = True

    def mapper(self, _, line):
        data = re.match(regex, line).groups()
        usuario = data[0]
        date = data[1]
        id = data[2]
        date_time = date[:20]
        epoch = time.mktime(time.strptime(date_time, pattern))
        yield usuario, (epoch, id)
            
    def reducer(self, usuario, data):
        sesiones = 0 #Offset for first
        comportamientos = {}
        time_prev = -10000 #Before epoch para que tengamos el principio
        for tiempo, id in data:
            if tiempo - time_prev > T:
                sesiones += 1
                comportamientos['comportamiento'+str(sesiones)] = set()
            time_prev = tiempo
            comportamientos['comportamiento'+str(sesiones)].add(id)
        for key, val in comportamientos.iteritems():
            comportamientos[key] = sorted(list(val))
        yield usuario, (sesiones, comportamientos) 
        
    #def steps(self):
    #    MRStep(mapper = self.mapper,
    #            reducer = self.reducer)
    #    MRStep(self.)
           
if __name__ == '__main__':
    MRLog_Info.run()