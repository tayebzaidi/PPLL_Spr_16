# -*- coding: utf-8 -*-
"""
Created on Thu May  5 10:58:30 2016

@author: alumno
"""


from mrjob.job import MRJob
from mrjob.step import MRStep
import string


class MRCharCount(MRJob):
    SORT_VALUES = True
    def mapper(self, _, line):
        stripped = line.translate(string.maketrans("",""), string.punctuation)
        for word in stripped.split():
            yield word.lower(), 1
        yield '.', len(stripped.split())
                
    def sum_words(self, word, counts):
        yield None, (word, sum(counts))
        
    
    def reducer(self, _, data):
        first = data.next()
        if(first[0] == '.'):
            total_word_count = first[1]
        for word, counts in data:
            yield word, counts/ float(total_word_count)

    def steps(self):
        return [
            MRStep(mapper = self.mapper,
                   reducer = self.sum_words),
            MRStep(reducer = self.reducer)
        ]

if __name__ == '__main__':
    MRCharCount.run()
    