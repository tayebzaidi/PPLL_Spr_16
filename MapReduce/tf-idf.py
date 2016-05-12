# -*- coding: utf-8 -*-
"""
Created on Tue May 10 12:32:06 2016

@author: alumno
"""

from mrjob.job import MRJob
from mrjob.step import MRStep
from mrjob.compat import jobconf_from_env
import string

class MRTF_IDF(MRJob):
    #SORT_VALUES = True

    def mapper(self, _, line):
        line_stripped = line.translate(string.maketrans("",""), string.punctuation)
        sentence = line_stripped.split()
        num_words = len(sentence)
        yield word, num_words
        yield '.total_counter.', num_words 
            
    def reducer(self, fichero, num_words):
        partial_sum = sum(num_words)
        self.increment_counter('group', 'total_words', partial_sum)
        yield None, (fichero, partial_sum)
        
    def filtro(self, _, data):
        first_value = data.next()
        assert first_value[0] == '.total_counter.'
        total = first_value[1]
        for fichero, counts in data:
            yield fichero, counts / float(total)
        
    def mapperPorFichero(self, _, line):
        pass
        
    def reducerPorFichero(self, key, values):
        pass
    
    def aggregatorFrequency(self, key, values):
        pass
    
    def steps(self):
        return [
            MRStep(mapper = self.mapper,
                    reducer = self.reducer),
            MRStep(reducer = self.filtro),
            MRStep(mapper = self.mapperPorFichero,
                    reducer = self.reducerPorFichero),
            MRStep(reducer + self.aggregatorFrequency)
        ]     


if __name__ == '__main__':
    print 'starting mrjob process'
    #....
    job = MRTF_IDF(args=['El_buscón-Quevedo.txt', 'MadameBovary.txt'])
    runner = job.make_runner()
    runner.run()
    tmp_output = []
    print 'Contador', runner.counters()
    for line in runner.stream_output():
        print '******parser', job.parse_output_line(line)
        tmp_output = tmp_output + [line]
        #...
    print 'Results:', tmp_output
    #...