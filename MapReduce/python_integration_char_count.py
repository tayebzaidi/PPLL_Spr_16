# -*- coding: utf-8 -*-
"""
Created on Tue May 10 12:18:02 2016

@author: alumno
"""


from mrjob.job import MRJob
import string


class MRCharCount(MRJob):

    def mapper(self, _, line):
        self.increment_counter('group', 'total_chars', len(line))
        yield "chars", len(line)
        
    
    def reducer(self, key, values):
        suma = sum(values)
        yield key, suma


if __name__ == '__main__':
    print 'starting mrjob process'
    #....
    job = MRCharCount(args=['El_buscón-Quevedo.txt', 'MadameBovary.txt'])
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
    