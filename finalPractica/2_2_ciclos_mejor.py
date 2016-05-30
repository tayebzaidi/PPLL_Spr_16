from mrjob.job import MRJob
from mrjob.step import MRStep
import string
import sys


class MRGrados(MRJob):
    SORT_VALUES = True    
    
    def mapper(self, _, line):
        line_stripped = line.translate(string.maketrans("",""), '"')
        line_split = line_stripped.split(',') #split by the comma
        sorted_line = sorted(line_split)
        node0 = sorted_line[0]
        node1 = sorted_line[1]
        if node0 != node1:  #eliminate edges with the same vertice
            yield (node0, node1), None  #eliminate duplicate nodes
        
        
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
        
class MRCiclos(MRJob):
    def mapper(self, _, line):
        line_split = line.split() #split by the comma)
        node0 = line_split[0]
        node1 = line_split[1]
        degree0 = line_split[2]
        degree1 = line_split[3]
        if degree0 <= degree1:
            yield node0, (node0, node1)
        else:
            yield node1, (node0, node1)
        yield '.pass_through.', (node0, node1, degree0, degree1)
        
    def reducer(self, key, values):
        if key != '.pass_through.':
            edges = list(values)
            if len(edges) > 1:
                for i in range(len(edges)):
                    for j in range(i, len(edges)):
                        if i != j:
                            if edges[i][0] and edges[j][1] != key:
                                yield (edges[i][0], edges[j][1]), edges[i]
        else:
            for node0, node1, degree0, degree1 in values:
                yield (node0, node1), 'original'
            
    def reducer2(self, key, values):
        vals = list(values)
        if len(vals) > 1:
            for val in vals:
                node0 = key[0]
                node1 = key[1]
                if val != 'original':
                    if val[0] in [node0, node1]:
                        node2 = val[1]
                    else:
                        node2 = val[0]
                    ciclo = [node0,node1,node2]
                    ciclo_sorted = sorted(ciclo)
                    yield ciclo_sorted, None
                    
        
    def steps(self):
        return [
            MRStep(mapper = self.mapper,
                    reducer = self.reducer),
            MRStep(reducer = self.reducer2)
        ]
        
if __name__=="__main__":
    print 'Starting grado_calcjob'
    job_grado_calc = MRGrados(args=sys.argv[1:])
    runner_grado_calc= job_grado_calc.make_runner()
    runner_grado_calc.run()
    grado_calc_output = []
    for line in runner_grado_calc.stream_output():
        grado_calc_output = grado_calc_output + [job_grado_calc.parse_output_line(line)]
    #print 'Results grado_calc:', grado_calc_output
    
    f = open('results_grado_calc.txt','w')
    for (node1, node2), (degree0, degree1) in grado_calc_output:
        f.write(str(node1)+'\t'+str(node2)+'\t'+str(degree0)+'\t'+str(degree1)+'\n')
    f.close()

    #print 'Starting ciclos_count job'
    job_ciclos_count  = MRCiclos(args=['results_grado_calc.txt'])
    runner_ciclos_count = job_ciclos_count.make_runner()
    runner_ciclos_count.run()
    ciclos_count_output = []
    for line in runner_ciclos_count.stream_output():
        ciclos_count_output = ciclos_count_output + [job_ciclos_count.parse_output_line(line)]
    for result in ciclos_count_output:
        print result
    