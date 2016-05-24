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
        if node1 != node2:
            str_node = ','.join([node1, node2])
            yield str_node, 1
        
        
    def reducer(self, key, values):
        yield None, key
    
    def grado_calc(self, key, values):
        grados = defaultdict(int)
        node_pairs = []
        for str_node in values:
            nodes = str_node.split(',')
            node1 = nodes[0]
            node2 = nodes[1]
            grados[node1] += 1
            grados[node2] += 1
            node_pair = [node1, node2]
            node_pairs.append(node_pair)
        for node_pair in node_pairs:
            yield node_pair, (grados[node_pair[0]], grados[node_pair[1]])
            
    def steps(self):
        return [
            MRStep(mapper = self.mapper,
                    reducer = self.reducer),
            MRStep(reducer = self.grado_calc)
        ]
            
        
if __name__=='__main__':
    sys.stderr = open('localerrorlog.txt', 'w')
    Grados.run()