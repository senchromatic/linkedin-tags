from collections import defaultdict
from directories import Directories
from operator import itemgetter
from os import listdir


class Processor:
	TOKEN_DELIMITER = ' '
	WORD_DELIMITER = ' '
	KEY_VALUE_DELIMITER = ':'
	
	def __init__(self, num_words=1):
		self.num_words = num_words
	
	@staticmethod
	def enlist_cleaned():
		target_dir = Directories.CLEANED_FOLDER
		return Directories.data_filenames(target_dir)
	
	def generate_frequencies(self, tokens):
		profile_frequencies = defaultdict(int)
		for i in xrange(len(tokens) - (self.num_words-1)):
			term = Processor.WORD_DELIMITER.join(tokens[i:(i+self.num_words)])
			profile_frequencies[term] += 1
		return profile_frequencies
	
	def count_frequencies(self, profile_string):
		tokens = profile_string.split(Processor.TOKEN_DELIMITER)
		return self.generate_frequencies(tokens)
	
	@staticmethod
	def tabulate_total_frequencies(role_frequencies):
		total_frequencies = defaultdict(int)
		for profile_frequencies in role_frequencies:
			for token,frequency in profile_frequencies.items():
				total_frequencies[token] += frequency
		return total_frequencies
	
	@staticmethod
	def calculate_proportions(frequencies):
		n_terms = float(sum(frequencies.values()))
		proportions = defaultdict(float)
		for token,frequency in frequencies.items():
			proportions[token] = frequency / n_terms
		return proportions
	
	@staticmethod
	def format_proportion(p):
		return Processor.KEY_VALUE_DELIMITER.join([p[0], str(p[1])])
	
	def process_cleaned(self, filename):
		with open(Directories.CLEANED_FOLDER + filename) as input:
			role_freq = []
			for line in input:
				role_freq.append(self.count_frequencies(line))
			total_freq = self.tabulate_total_frequencies(role_freq)
			props = Processor.calculate_proportions(total_freq)
			ranklist = sorted(props.items(), key=itemgetter(1), reverse=True)
			formatted = map(Processor.format_proportion, ranklist)
		target_dir = Directories.PROCESSED_FOLDER + Directories.subdirectory_name(self.num_words)
		Directories.create_directory(target_dir)
		with open(target_dir + filename, 'w') as output:
			n_terms = sum(total_freq.values())  # total number of terms
			output.write(str(n_terms) + '\n')
			for s in formatted:
				output.write(s + '\n')
	
	def process_all_cleaned(self):
		for filename in Processor.enlist_cleaned():
			print('\t' + filename)
			self.process_cleaned(filename)


if __name__ == '__main__':
	max_num_words = input('Maximum number of consecutive words to consider as a term: ')
	processor = Processor()
	for num_words in xrange(max_num_words):
		print('processing ' + Directories.subdirectory_name(num_words+1) + '...')
		processor.num_words = num_words+1
		processor.process_all_cleaned()
