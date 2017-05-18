from os import makedirs, path


class Directories:
	RAW_FOLDER = 'raw/'
	CLEANED_FOLDER = 'cleaned/'
	PROCESSED_FOLDER = 'processed/'
	RESULTS_FOLDER = 'results/'
	
	@staticmethod
	def subdirectory_name(num_words):
		return 'l' + str(num_words) + '/'
	
	@staticmethod
	def create_directory(target):
		if not path.exists(target):
			makedirs(target)
