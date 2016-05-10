from mrjob.job import MRJob
from mrjob.step import MRStep
import string

class MRIdxLabel(MRJob):

    def mapper(self, _, line):
        line_stripped = line.translate()
        sentence_total = line_stripped.split()
        line_number = int(sentence_total[0])
        sentence = sentence_total[1:]
        for word in sentence:
            if len(word) > 5:
                yield word.lower(), line_number 
            
    def reducer(self, word, line_num):
        #line = sum(line_num)
        indices = []
        for line_idx in line_num:
            if line_num not in indices:
                indices.append(line_idx)
        yield word, indices

    #def inv_idx(self, _, data):
    #    indices = []
    #    for w, idx in data:
    #        word = w
    #        indices.append((word, idx))
    #    yield word, indices

    #def steps(self):
    #    return [
    #        MRStep(mapper = self.mapper,
    #                reducer = self.reducer),
    #        MRStep(reducer = self.inv_idx)
    #    ]

if __name__ == '__main__':
    MRIdxLabel.run()
