# -*- coding: utf-8 -*-
"""
Created on Thu May 12 10:30:03 2016

@author: alumno
"""

from mrjob.job import MRJob
from mrjob.step import MRStep
from mrjob.compat import jobconf_from_env
import string

class MRIdxLabel(MRJob):
    #SORT_VALUES = True

    def mapper(self, _, line):
        yield 'total', jobconf_from_env('map.input.file')
            
    def reducer(self, key, ficheros):
        yield None, len(set(ficheros))
    
        
if __name__ == '__main__':
    MRIdxLabel.run()

