from google_search import Google
from linkedin_service import LinkedIn
from document_manager import Database


class Retriever:
	RESULTS_PER_PAGE = 10
	
	def __init__(self, query=None):
		Database.setup_encoding()
		self.linkedin = LinkedIn()
		self.query = query
	
	def process(self, urls):
		for url in urls:
			profile = self.linkedin.download_profile(url)
			tokens = Database.tokenize(profile)
			Database.save_local(tokens, self.query)
	
	# returns whether the operation was successful
	# start_page : non-negative integer
	def download(self, start_page):  
		index = start_page * Retriever.RESULTS_PER_PAGE
		urls = Google.get_profile_urls(self.query, index)
		self.process(urls)
		if urls:
			return True
		return False

