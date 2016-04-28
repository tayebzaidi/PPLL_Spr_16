from mrjob.job import MRJob

class MRCharCount(MRJob):

    def mapper(self, _, line):
        self.increment_counter('group', 'total_chars', len(line))
        yield "chars", len(line)
            
    def reducer(self, key, values):
        yield key, sum(values)


if __name__ == '__main__':
    MRCharCount.run()
