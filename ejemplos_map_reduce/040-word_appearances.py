from mrjob.job import MRJob
import string 

class MRWordAppearances(MRJob):
   
    def mapper(self, _, line):
        for x in string.punctuation:
            line = line.replace(x,' ')
        for word in line.split():
            yield (word.lower(), 1)

    def reducer(self, word, counts):
        yield word, sum(counts)

if __name__ == '__main__':
    MRWordAppearances.run()
