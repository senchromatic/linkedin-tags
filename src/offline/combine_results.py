from directories import Directories
from operator import itemgetter
from os import listdir


class Combiner:
	def __init__(self, document):
		self.document = document
		self.corpus = {}
	
	@staticmethod
	def enlist_analyzed():
		target_dir = Directories.RESULTS_FOLDER + Directories.subdirectory_name(1)
		return Directories.data_filenames(target_dir)
	
	def process(self, line):
		term_ratio = line.split(',')
		if len(term_ratio) != 2:
			return None
		term = term_ratio[0]
		ratio = float(term_ratio[1])
		self.corpus[term] = ratio
	
	def include_subcorpus(self, num_words):
		target_dir = Directories.RESULTS_FOLDER + Directories.subdirectory_name(num_words)
		with open(target_dir + self.document) as input:
			input.readline()  # skip header row
			for line in input:
				result = self.process(line)
	
	def save_corpus(self):
		target_dir = Directories.RESULTS_FOLDER + Directories.COMBINED_SUBFOLDER
		Directories.create_directory(target_dir)
		with open(target_dir + self.document, 'w') as output:
			output.write(Directories.HEADER_ROW)
			ranklist = sorted(self.corpus.items(), key=itemgetter(1), reverse=True)
			for term_ratio in ranklist:
				output.write(term_ratio[0] + ',' + str(term_ratio[1]) + '\n')


if __name__ == '__main__':
	max_num_words = input('Maximum number of consecutive words to consider as a term: ')
	documents = Combiner.enlist_analyzed()
	for document in documents:
		print('combining results from ' + document)
		combine = Combiner(document)
		for num_words in xrange(max_num_words):
			print('\tincluding ' + Directories.subdirectory_name(num_words+1) + '...')
			combine.include_subcorpus(num_words+1)
		combine.save_corpus()
