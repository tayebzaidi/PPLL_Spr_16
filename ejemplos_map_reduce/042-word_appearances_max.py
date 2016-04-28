from mrjob.job import MRJob
from mrjob.step import MRStep
import string 

class MRWordAppearances(MRJob):

    def mapper(self, _, line):
        for x in string.punctuation:
            line = line.replace(x,' ')
        for word in line.split():
            yield (word.lower(), 1)

    def sum_words(self, word, counts):
        yield None, (sum(counts), word)

    def reducer(self, _, values):
        max = 0
        max_word = ''
        for (counts,word) in values:
            if counts > max:
                max = counts
                max_word = word 
        yield max_word, max

    def steps(self):
        return [
            MRStep(mapper = self.mapper,
                    reducer = self.sum_words),
            MRStep(reducer = self.reducer) 
        ]

if __name__ == '__main__':
    MRWordAppearances.run()
