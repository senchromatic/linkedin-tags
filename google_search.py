from datetime import datetime
from document_manager import Database
from time import sleep


class Google:
	BASE_URL = 'https://www.google.com/search?q=site%3Alinkedin.com+'
	START_NAME = '&start='
	USER_SUBDOMAIN = 'linkedin.com/in/'
	SAFE_DELAY = 5.0
	
	def __init__(self):
		self.last_visit = None
	
	@staticmethod
	def get_profile_urls(self, query, start):
		if self.last_visit:
			time_difference = datetime.now() - self.last_visit
			remaining = max(0, Google.SAFE_DELAY - time_difference.total_seconds())
			sleep(remaining)
		self.last_visit = datetime.now()
		start_value = str(start)
		soup = Database.download_dom(Google.BASE_URL + query + Google.START_NAME + start_value)
		results = soup.findAll('div', {'class' : 'g'})
		urls = []
		for result in results:
			link = result.find('cite')
			if not link:
				continue
			url = link.text
			if Google.USER_SUBDOMAIN in url:
				urls.append(url)
		return urls
