from datetime import datetime
from document_manager import Database
from selenium.webdriver.common.by import By
from time import sleep
from web_utilities import Utility


class Google:
	BASE_URL = 'https://www.google.com/search?q=site%3Alinkedin.com/in+'
	START_NAME = '&start='
	USER_SUBDOMAIN = 'linkedin.com/in/'
	MAX_TIMEOUT = 20
	SAFE_DELAY = 10.0
	RELOAD_DELAY = 1.0
	MICROSLEEPS = 10
	SCROLL = False
	
	def __init__(self, browser):
		self.last_visit = None
		self.browser = browser
	
	def get_profile_urls(self, query, start):
		if self.last_visit:
			time_difference = datetime.now() - self.last_visit
			remaining = max(0, Google.SAFE_DELAY - time_difference.total_seconds())
			sleep(remaining)
		self.last_visit = datetime.now()
		start_value = str(start)
		soup = Utility.make_soup(self, Google.BASE_URL + query + Google.START_NAME + start_value, (By.CLASS_NAME, 'g'))
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
