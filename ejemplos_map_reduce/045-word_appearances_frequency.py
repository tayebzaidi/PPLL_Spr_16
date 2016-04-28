from mrjob.job import MRJob
from mrjob.step import MRStep

import string 

class MRWordAppearances(MRJob):

    def mapper(self, _, line):
        for x in string.punctuation:
            line = line.replace(x,' ')
        for word in line.split():
            yield (word.lower(), 1)

    def reducer(self, word, counts):
        yield None, (word, sum(counts))
    
    def frequency(self, _, data):
        total = 0
        words = []
        for word, counts in data:
            total += counts
            words.append((word,counts))
        for word, counts in words: ##! No funciona con data, es un generador!
            yield word, counts/float(total)

    def steps(self):
        return [
            MRStep(mapper = self.mapper,
                    reducer = self.reducer),
            MRStep(reducer = self.frequency) 
        ]

if __name__ == '__main__':
    MRWordAppearances.run()
