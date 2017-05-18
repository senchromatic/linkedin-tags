from collections import defaultdict
from data_processing import Processor
from directories import Directories
from math import sqrt
from operator import itemgetter
from os import listdir
from statsmodels.stats.proportion import proportion_confint


class Analysis:
	EPSILON = 1e-10  # don't use absolute smallest, leave some room for error
	
	def __init__(self, num_words, alpha=0.01):
		self.proportions = {}
		self.ratios = {}
		self.n_terms = {}
		self.num_words = num_words
		self.alpha = alpha
		self.corpus = None
		self.overall_ci = {}
	
	# cached storage
	def load_proportions(self, document):
		if document not in self.proportions:
			proportions = {}
			target_dir = Directories.PROCESSED_FOLDER + Directories.subdirectory_name(self.num_words)
			with open(target_dir + document) as input:
				self.n_terms[document] = int(input.readline())
				for line in input:
					kv = line.split(Processor.KEY_VALUE_DELIMITER)
					term = kv[0]
					try:
						prop = float(kv[1])
					except:
						prop = 0.0
					proportions[term] = prop
			self.proportions[document] = proportions
		return self.proportions[document]
	
	@staticmethod
	# vector length (Euclidean distance)
	def l2norm(d):
		return sqrt(sum([v*v for v in d.values()]))
	
	def cosine_similarity(self, document1, document2):
		prop1 = self.load_proportions(document1)
		prop2 = self.load_proportions(document2)
		numerator = sum([(0.0 if term not in prop2 else prop1[term]*prop2[term]) for term in prop1.keys()])
		denominator = Analysis.l2norm(prop1) * Analysis.l2norm(prop2)
		return numerator / denominator
	
	@staticmethod
	def enlist_processed(num_words):
		target_dir = Directories.PROCESSED_FOLDER + Directories.subdirectory_name(num_words)
		return listdir(target_dir)  # relative filenames

	def load_all_documents(self):
		for document in Analysis.enlist_processed(self.num_words):
			self.load_proportions(document)
	
	def create_corpus(self):
		self.total_terms = sum(self.n_terms.values())
		self.corpus = defaultdict(float)
		for document,n_terms in self.n_terms.items():
			representation = float(n_terms) / self.total_terms
			proportions = self.proportions[document]
			for term,proportion in proportions.items():
				overall_prop = proportion * representation
				self.corpus[term] += overall_prop
	
	def confidence_interval(self, term, proportions, n_terms):
		p = proportions[term] if term in proportions else 0.0
		successes = round(p * n_terms)
		nobs = n_terms
		confint = proportion_confint(successes, nobs, alpha=self.alpha, method='agresti_coull')
		lower = min(confint)
		upper = max(confint)
		return (max(Analysis.EPSILON, lower), min(upper, 1.0))
	
	def get_overall_ci(self, term):
		if term not in self.overall_ci:
			self.overall_ci[term] = self.confidence_interval(term, self.corpus, self.total_terms)
		return self.overall_ci[term]
	
	def likelihood_ratio(self, term, document):
		if not self.corpus:
			self.create_corpus()
		ci_doc = self.confidence_interval(term, self.proportions[document], self.n_terms[document])
		ci_corpus = self.get_overall_ci(term)
		return (min(ci_doc) / max(ci_corpus), max(ci_doc) / min(ci_corpus))
	
	def compute_likelihood_ratios(self, document):
		ratios = {}
		for term in self.proportions[document].keys():
			ratio = self.likelihood_ratio(term, document)
			conservative = min(ratio)
			ratios[term] = conservative
		ranklist = sorted(ratios.items(), key=itemgetter(1), reverse=True)
		self.ratios[document] = ranklist
	
	def generate_all_results(self):
		for document in Analysis.enlist_processed(self.num_words):
			print('\t' + document)
			self.compute_likelihood_ratios(document)
			target_dir = Directories.RESULTS_FOLDER + Directories.subdirectory_name(self.num_words)
			Directories.create_directory(target_dir)
			with open(target_dir + document, 'w') as output:
				output.write(Directories.HEADER_ROW)
				for term_ratio in self.ratios[document]:
					term = term_ratio[0]
					ratio = term_ratio[1]
					output.write(term + ',' + str(ratio) + '\n')

if __name__ == '__main__':
	max_num_words = input('Maximum number of consecutive words to consider as a term: ')
	for num_words in xrange(max_num_words):
		print('analyzing ' + Directories.subdirectory_name(num_words+1) + '...')
		analysis = Analysis(num_words+1)
		analysis.load_all_documents()
		analysis.generate_all_results()
