# -*- coding: utf-8 -*-
"""
Created on Tue May 10 11:36:09 2016

@author: alumno
"""

from mrjob.job import MRJob
from mrjob.step import MRStep
from mrjob.compat import jobconf_from_env
import string

class MRIdxLabel(MRJob):
    #SORT_VALUES = True

    def mapper(self, _, line):
        line_stripped = line.translate(string.maketrans("",""), string.punctuation)
        sentence = line_stripped.split()
        num_words = len(sentence)
        yield jobconf_from_env('map.input.file'), num_words
        yield '.total_counter.', num_words 
            
    def reducer(self, fichero, num_words):
        partial_sum = sum(num_words)
        yield None, (fichero, partial_sum)
        
    def filtro(self, _, data):
        first_value = data.next()
        assert first_value[0] == '.total_counter.'
        total = first_value[1]
        for fichero, counts in data:
            yield fichero, (counts, total)
        
    def steps(self):
        return [
            MRStep(mapper = self.mapper,
                    reducer = self.reducer),
            MRStep(reducer = self.filtro) 
        ]     
        
if __name__ == '__main__':
    MRIdxLabel.run()

