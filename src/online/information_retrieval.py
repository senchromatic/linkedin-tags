from google_search import Google
from linkedin_service import LinkedIn
from document_manager import Database
from selenium import webdriver


class Retriever:
	RESULTS_PER_PAGE = 10
	MAX_PAGES = 1000
	FAILSAFE_THRESHOLD = 10
	
	def __init__(self, query=None):
		Database.setup_encoding()
		self.browser = webdriver.Firefox()
		self.google = Google(self.browser)
		self.linkedin = LinkedIn(self.browser)
		self.query = query
	
	def process(self, urls):
		for url in urls:
			profile = self.linkedin.download_profile(url)
			if not profile:
				continue
			tokens = Database.tokenize(profile)
			Database.save_local(tokens, self.query)
	
	# returns whether the operation was successful
	# start_page : non-negative integer
	def download(self, start_page):  
		index = start_page * Retriever.RESULTS_PER_PAGE
		urls = self.google.get_profile_urls(self.query, index)
		self.process(urls)
		if urls:
			return True
		return False
	
	def download_all_data(self, query=None):
		if query:
			self.query = query
		consecutive_fails = 0
		for page in xrange(Retriever.MAX_PAGES):
			print('Downloading page ' + str(page))
			if self.download(page):
				consecutive_fails = 0
			else:
				consecutive_fails += 1
			if consecutive_fails > Retriever.FAILSAFE_THRESHOLD:
				print('Unable to find more profiles')
				break

