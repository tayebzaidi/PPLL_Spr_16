# -*- coding: utf-8 -*-
"""
Created on Tue May 17 12:09:08 2016

@author: alumno
"""
from mrjob.job import MRJob
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
        print regex
        print line
        data = re.match(regex, line).groups()
        usuario = data[0]
        date = data[1]
        date_time = date[:20]
        epoch = time.mktime(time.strptime(date_time, pattern))
        yield usuario, epoch
            
    def reducer(self, usuario, horas):
        sesiones = -1 #Offset for first 
        time_prev = 0
        for tiempo in horas:
            if (tiempo - time_prev) > T:
                sesiones  += 1
            time_prev = time
        yield usuario, sesiones
    
        
if __name__ == '__main__':
    MRLog_Info.run()
