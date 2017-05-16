from bs4 import BeautifulSoup
import re
import requests
import sys

class Database:
	OUTPUT_DIRECTORY = "data/"
	
	@staticmethod
	def setup_encoding():
		reload(sys)
		sys.setdefaultencoding('utf-8')
	
	@staticmethod
	def download_dom(url):
		html = requests.get(url).content
		return BeautifulSoup(html, 'lxml')
	
	@staticmethod
	def tokenize(dom):
		return dom.text.split()
	
	@staticmethod
	def save_local(tokens, query):
		plus_to_underscore = re.sub(r'\+', '_', query)
		only_word_characters = re.sub(r'\W+', '', plus_to_underscore)
		filename = only_word_characters + '.txt'
		path = Database.OUTPUT_DIRECTORY + filename
		with open(path, 'a') as output:
			output.write(' '.join(tokens) + '\n')
