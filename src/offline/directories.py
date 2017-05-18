from os import makedirs, path


class Directories:
	RAW_FOLDER = 'raw/'
	CLEANED_FOLDER = 'cleaned/'
	PROCESSED_FOLDER = 'processed/'
	RESULTS_FOLDER = 'results/'
	COMBINED_SUBFOLDER = 'combined/'
	FILTERED_FOLDER = 'filtered/'
	HEADER_ROW = 'term,likelihood_ratio\n'
	IGNORE = ['.keep']
	
	@staticmethod
	def subdirectory_name(num_words):
		return 'l' + str(num_words) + '/'
	
	@staticmethod
	def create_directory(target):
		if not path.exists(target):
			makedirs(target)
	
	@staticmethod
	def is_data(filename):
		return filename not in Directories.IGNORE
