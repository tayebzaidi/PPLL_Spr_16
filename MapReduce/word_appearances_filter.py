# -*- coding: utf-8 -*-
"""
Created on Thu May  5 10:40:29 2016

@author: alumno
"""

from mrjob.job import MRJob
import string


class MRCharCount(MRJob):

    def mapper(self, _, line):
        stripped = line.translate(string.maketrans("",""), string.punctuation)
        for word in stripped.split():
            if len(word) >  3:
                yield word.lower(), 1
        
    
    def reducer(self, key, values):
        suma = sum(values)
        if suma > 50:
            yield key, suma


if __name__ == '__main__':
    MRCharCount.run()
    