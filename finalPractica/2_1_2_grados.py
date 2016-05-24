from mrjob.job import MRJob
from mrjob.step import MRStep
from collections import defaultdict

class Grados(MRJob):
    def mapper(self, _, line):
        line_split = line.strip('()').split(',') #Strip parenthesis and split by the comma
        sorted_line = sorted(line_split)
        node1 = sorted_line[0]
        node2 = sorted_line[1]
        if node1 != node2:
            str_node = ','.join([node1, node2])
            yield None, str_node
        
        
    def reducer(self, key, values):
        aristas = []
        for val in values:
            if val not in aristas:
                aristas.append(val)
                node1 = val[0]
                node2 = val[2]
                yield None, (node1, node2)
    
    def grado_calc(self, key, values):
        grados = defaultdict(int)
        node_pairs = []
        for node1, node2 in values:
            print node1
            grados[node1] += 1
            grados[node2] += 1
            node_pair = [node1, node2]
            node_pairs.append(node_pair)
        print grados
        for node_pair in node_pairs:
            yield None, (node_pair, grados[node_pair[0]], grados[node_pair[1]])
            
    def steps(self):
        return [
            MRStep(mapper = self.mapper,
                    reducer = self.reducer),
            MRStep(reducer = self.grado_calc)
        ]
            
        
if __name__=='__main__':
    Grados.run()