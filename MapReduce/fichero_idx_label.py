# -*- coding: utf-8 -*-
"""
Created on Tue May 10 11:23:39 2016

@author: alumno
"""
from mrjob.job import MRJob
from mrjob.step import MRStep
from mrjob.compat import jobconf_from_env
import string

class MRIdxLabel(MRJob):

    def mapper(self, _, line):
        line_stripped = line.translate(string.maketrans("",""), string.punctuation)
        sentence = line_stripped.split()
        for word in sentence:
            if len(word) > 1:
                yield word.lower(), jobconf_from_env('map.input.file')
            
    def reducer(self, word, line_num):
        #line = sum(line_num)
        indices = []
        for file_idx in line_num:
            if file_idx not in indices:
                indices.append(file_idx)
        yield word, indices
        
    def filtro(self, word, indices):
        if len(indices) > 1:
            pass
        
        
        
if __name__ == '__main__':
    MRIdxLabel.run()

