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
        for word in sentence:
            yield (word.lower(), jobconf_from_env('map.input.file')), 1
        #yield '.total_counter.', num_words
            
    def reducer(self, key, values):
        N = sum(values)
        word = key[0]
        yield word, (key[1], N)
        
    def filtro(self, word, data):
        ficheros_unique = []
        term_frec = []
        for fichero, counts in data:
            if fichero not in ficheros_unique:
                ficheros_unique.append(fichero)
            term_frec.append((fichero, counts))
        K = len(ficheros_unique)
        for (fichero, counts) in term_frec:    
            yield (word, fichero), (counts, K)
    
    def steps(self):
        return [
            MRStep(mapper = self.mapper,
                    reducer = self.reducer),
            MRStep(reducer = self.filtro),
        ]     


if __name__ == '__main__':
    print 'starting mrjob process'
    #....
    job = MRTF_IDF(args=['a.txt', 'b.txt', 'c.txt'])
    runner = job.make_runner()
    runner.run()
    tmp_output = []
    print 'Contador', runner.counters()
    for line in runner.stream_output():
        print '******parser', job.parse_output_line(line)
        tmp_output = tmp_output + [line]
        #...
    print 'Results:', tmp_output
    print len(tmp_output)
    #...