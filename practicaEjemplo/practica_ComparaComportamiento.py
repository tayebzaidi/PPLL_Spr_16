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
                for val in comportamientos.values():
                    comportamiento = sorted(list(val))
                    yield comportamiento, usuario
        
    def compara(self, comportamiento, usuarios):
        user_list = list(set(usuarios))
        yield comportamiento, user_list
            
            
    def steps(self):
        return [
            MRStep(mapper = self.mapper,
                    reducer = self.reducer),
            MRStep(reducer = self.compara)
        ]
           
if __name__ == '__main__':
    MRLog_Info.run()