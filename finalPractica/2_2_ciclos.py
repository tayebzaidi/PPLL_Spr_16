from mrjob.job import MRJob
from mrjob.step import MRStep
from collections import defaultdict
import string
import sys

class Ciclos(MRJob):
    def mapper(self, _, line):
        if line[0] != '#':
            line_stripped = line.translate(string.maketrans("",""), '"') #Eliminar los '"'
            line_split = line_stripped.split(',') #split by the comma
            sorted_line = sorted(line_split)
            node1 = sorted_line[0]
            node2 = sorted_line[1]
            if node1 != node2:
                yield (node1, node2), None
                yield '.pass_through.', (node1, node2)
        
    def reducer(self, key, values):
        if key != '.pass_through.':
            yield key[0], key[1]
        else:
            for val in values:
                yield '.pass_through.', val
        
    def reducer2(self, key, values):
        if key != '.pass_through.':
            nodes = list(values)
            if len(nodes) > 1:
                for i in range(len(nodes)):
                    for j in range(i, len(nodes)):
                        if i != j:
                            yield (nodes[i], nodes[j]), key
        else:
            for node1, node2 in values:
                yield (node1, node2), 'original'
            
    def reducer3(self, key, values):
        vals = list(values)
        if len(vals) > 1:
            for val in vals:
                node1 = key[0]
                node2 = key[1]
                if val != 'original':
                    node3 = val
                    ciclo = [node1,node2,node3]
                    ciclo_sorted = sorted(ciclo)
                    yield ciclo_sorted, None
                    
        
    def steps(self):
        return [
            MRStep(mapper = self.mapper,
                    reducer = self.reducer),
            MRStep(reducer = self.reducer2),
            MRStep(reducer = self.reducer3)
        ]
            
                

            
        
if __name__=='__main__':
    #print 'Starting ciclos1 job'
    sys.stderr = open('localerrorlog.txt', 'w')
    Ciclos.run()
    