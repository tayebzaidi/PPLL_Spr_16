# -*- coding: utf-8 -*-
"""
Created on Tue May 10 12:09:09 2016

@author: alumno
"""

from mrjob.job import MRJob
from mrjob.compat import jobconf_from_env
import string

class MRCharCount(MRJob):
    
    def  mapper(self, _, line):
        n = len(line)
        self.increment_counter('group', 'total_chars', n)
        yield jobconf_from_env('map.input.file'), n
        
    def reducer(self, file, chars):
        yield file, sum(chars)
        
        
if __name__ == '__main__':
    MRCharCount.run()