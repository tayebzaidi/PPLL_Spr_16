from mrjob.job import MRJob
from mrjob.step import MRStep
import string
import sys

class Simplificar(MRJob):
    def mapper(self, _, line):
        line_stripped = line.translate(string.maketrans("",""), '"')
        line_split = line_stripped.split(',') #split by the comma
        sorted_line = sorted(line_split)
        node1 = sorted_line[0]
        node2 = sorted_line[1]
        if node1 != node2:
            str_node = ','.join([node1,node2])
            yield None, str_node
        
        
    def reducer(self, key, values):
        aristas = set()
        for val in values:
            aristas.add(val)
        return_aristas = sorted(list(aristas))
        yield return_aristas, 1
        
if __name__=='__main__':
    sys.stderr = open('localerrorlog.txt', 'w')
    Simplificar.run()