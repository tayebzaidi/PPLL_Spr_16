from mrjob.job import MRJob
from mrjob.step import MRStep
from collections import defaultdict
import sys

class Ciclos_Paso1(MRJob):
    def mapper(self, _, line):
        if line[0] != '#':
            line_split = line.strip('()').split(',') #Strip parenthesis and split by the comma
            sorted_line = sorted(line_split)
            node1 = sorted_line[0]
            node2 = sorted_line[1]
            if node1 != node2:
                yield node1, node2
        
        
    def reducer(self, key, values):
        nodes = list(values)
        for i in range(len(nodes)):
            for j in range(i, len(nodes)):
                if key != '"A"':
                    print key, i, j   
                if i != j:
                    yield (nodes[i], nodes[j]), key
        
            
      
class Ciclos_Paso2(MRJob):
    def ciclos_count(self, key, values):
            pass
    
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
            yield node_pair, (grados[node_pair[0]], grados[node_pair[1]])
            
        for node in node_connections.keys():
            if len(node_connections[node]) > 1:
                for node_sub in node_connections[node]:
                    if node in node_connections[node_sub]:
                        pass
            
    def ciclos_count(self, key, values):
        pass
            
    def steps(self):
        return [
            MRStep(mapper = self.mapper,
                    reducer = self.reducer)#,
            #MRStep(reducer = self.grado_calc)
        ]
            
        
if __name__=='__main__':
    print 'Starting ciclos1 job'
    job_ciclos1 = Ciclos_Paso1(args=sys.argv[1:])
    runner_ciclos1 = job_ciclos1.make_runner()
    runner_ciclos1.run()
    ciclos1_output = []
    for line in runner_ciclos1.stream_output():
        ciclos1_output = ciclos1_output + [job_ciclos1.parse_output_line(line)]
    print 'Results ciclos1:', ciclos1_output
    
    f = open('results_ciclos1.txt','w')
    for (node1, node2), parent in ciclos1_output:
        f.write(node1+'\t'+node2+'\t'+parent+'\n')
    f.close()