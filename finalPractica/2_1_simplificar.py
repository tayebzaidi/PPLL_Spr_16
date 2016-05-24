from mrjob.job import MRJob
from mrjob.step import MRStep

class Simplificar(MRJob):
    def mapper(self, _, line):
        line_split = line.strip('()').split(',') #Strip parenthesis and split by the comma
        sorted_line = sorted(line_split)
        node1 = sorted_line[0]
        node2 = sorted_line[1]
        if node1 != node2:
            str_node = ','.join([node1, node2])
            yield None, str_node
        
        
    def reducer(self, key, values):
        aristas = set()
        for val in values:
            aristas.add(val)
        yield key, list(aristas)
        
if __name__=='__main__':
    Simplificar.run()