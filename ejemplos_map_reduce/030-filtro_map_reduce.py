# -*- coding: utf-8 -*-

from mrjob.job import MRJob


class MRFiltroMapReduce(MRJob):

    def mapper(self, _, line):
        if 'map' in line.lower():
            yield "sí", 1
        else:
            yield "no", 1
    
    def reducer(self, key, values):
        yield key, sum(values)

if __name__ == '__main__':
    MRFiltroMapReduce.run()
    
