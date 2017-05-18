from directories import Directories
from operator import itemgetter
from os import listdir


class Terms:
	def __init__(self):
		self.terms = set()
	
	@staticmethod
	def enlist_termfiles():
		all_files = listdir(Directories.TERMS_FOLDER)
		return Directories.only_data(all_files)
	
	def include_shortlist(self, shortlist):
		target_dir = Directories.TERMS_FOLDER
		with open(target_dir + shortlist) as input:
			for line in input:
				term = line.strip()
				self.terms.add(term)
	
	def include_all_shortlists(self):
		for termfile in Terms.enlist_termfiles():
			self.include_shortlist(termfile)


class Filterer:
	def __init__(self, document):
		self.document = document
		self.corpus = {}
	
	@staticmethod
	def enlist_combined():
		all_files = listdir(Directories.RESULTS_FOLDER + Directories.COMBINED_SUBFOLDER)
		return Directories.only_data(all_files)
	
	def process(self, line, terms_list):
		term_ratio = line.split(',')
		if len(term_ratio) != 2:
			return None
		term = term_ratio[0]
		if term not in terms_list.terms:
			return False
		ratio = float(term_ratio[1])
		self.corpus[term] = ratio
	
	def load_corpus(self, terms_list):
		target_dir = Directories.RESULTS_FOLDER + Directories.COMBINED_SUBFOLDER
		with open(target_dir + self.document) as input:
			input.readline()  # skip header row
			for line in input:
				result = self.process(line, terms_list)
	
	def save_filtered(self):
		target_dir = Directories.FILTERED_FOLDER
		Directories.create_directory(target_dir)
		with open(target_dir + self.document, 'w') as output:
			output.write(Directories.HEADER_ROW)
			ranklist = sorted(self.corpus.items(), key=itemgetter(1), reverse=True)
			for term_ratio in ranklist:
				output.write(term_ratio[0] + ',' + str(term_ratio[1]) + '\n')


if __name__ == '__main__':
	all_terms = Terms()
	all_terms.include_all_shortlists()

	documents = Filterer.enlist_combined()
	for document in documents:
		print('filtering results from ' + document)
		filterer = Filterer(document)
		filterer.load_corpus(all_terms)
		filterer.save_filtered()
