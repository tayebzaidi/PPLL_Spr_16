from mrjob.job import MRJob
from mrjob.step import MRStep
from collections import defaultdict
import string
import sys

class Grados(MRJob):
    SORT_VALUES = True    
    
    def mapper(self, _, line):
        line_stripped = line.translate(string.maketrans("",""), '"')
        line_split = line_stripped.split(',') #split by the comma
        sorted_line = sorted(line_split)
        node1 = sorted_line[0]
        node2 = sorted_line[1]
        if node1 != node2:  #eliminate edges with the same vertice
            yield (node1, node2), None  #eliminate duplicate nodes
        
        
    def reducer(self, key, values):
        yield key[0], key
        yield key[1], key
        
    def sift(self, key, values):
        degree = 0
        send_edges = []
        for val in values:
            degree += 1
            if val not in send_edges:
                send_edges.append(val)
        for edge in sorted(send_edges):
            if key == edge[0]:
                location = 0
            elif key == edge[1]:
                location = 1
            yield edge, (edge, degree, location)    
        
    
    def grado_calc(self, key, values):
        for edge, degree, location in values:
            if location == 0:
                degree0 = degree
            if location == 1:
                degree1 = degree
        yield edge, (degree0, degree1)

            
    def steps(self):
        return [
            MRStep(mapper = self.mapper,
                    reducer = self.reducer),
            MRStep(reducer = self.sift),
            MRStep(reducer = self.grado_calc)
        ]
            
        
if __name__=='__main__':
    sys.stderr = open('localerrorlog.txt', 'w')
    Grados.run()