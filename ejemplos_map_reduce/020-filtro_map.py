# -*- coding: utf-8 -*-

from mrjob.job import MRJob


class MRFiltroMap(MRJob):

    def mapper(self, _, line):
        if 'map' in line:
            yield "sí", line 
        else:
            yield "no", line

if __name__ == '__main__':
    MRFiltroMap.run()
