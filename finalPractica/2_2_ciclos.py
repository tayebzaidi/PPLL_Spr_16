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
            yield node1, node2
        
        
    def reducer(self, key, values):
        nodes = list(values)
        for node1 in nodes:
            nodes_sliced = nodes[nodes.index(node1)+1:]
            for node2 in nodes.remove(node1):
                nodes.append(node)
                yield key, (node1, node2)
        for node in nodes:
            nodes_temp = list(nodes)
            nodes_sliced = nodes_temp[nodes_temp.index(node)+1:]
            yield node, (','.join(nodes_sliced), key)
            
    def ciclos_count(self, key, values):
        for str_nodes, parent_node
    
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
                    if node in node_connections[node_sub]
            
    def ciclos_count(self, key, values):
        pass
            
    def steps(self):
        return [
            MRStep(mapper = self.mapper,
                    reducer = self.reducer)#,
            #MRStep(reducer = self.grado_calc)
        ]
            
        
if __name__=='__main__':
    Grados.run()