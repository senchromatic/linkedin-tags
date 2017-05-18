from directories import Directories
from os import listdir
from string import punctuation


class Cleaner:
	@staticmethod
	def enlist_raws():
		all_files = listdir(Directories.RAW_FOLDER)  # relative filenames
		return filter(Directories.is_data, all_files)
	
	@staticmethod
	def clean_string(original):
		no_punctuation = original.translate(None, punctuation)
		return no_punctuation.lower()
	
	@staticmethod
	def clean_raw(filename):
		with open(Directories.RAW_FOLDER + filename) as input:
			with open(Directories.CLEANED_FOLDER + filename, 'w') as output:
				for line in input:
					output.write(Cleaner.clean_string(line))
	
	@staticmethod
	def clean_all_raws():
		for filename in Cleaner.enlist_raws():
			Cleaner.clean_raw(filename)

if __name__ == '__main__':
	Cleaner.clean_all_raws()
