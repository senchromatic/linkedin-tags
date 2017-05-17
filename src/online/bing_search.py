from datetime import datetime
from document_manager import Database
from selenium.webdriver.common.by import By
from time import sleep
from web_utilities import Utility


class Bing:
	BASE_URL = 'https://bing.com/?q=site:linkedin.com/in+'
	START_NAME = '&first='
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
			remaining = max(0, Bing.SAFE_DELAY - time_difference.total_seconds())
			sleep(remaining)
		self.last_visit = datetime.now()
		start_value = str(start)
		soup = Utility.make_soup(self, Bing.BASE_URL + query + Bing.START_NAME + start_value, (By.CLASS_NAME, 'b_algo'))
		results = soup.findAll('li', {'class' : 'b_algo'})
		urls = []
		for result in results:
			link = result.find('cite')
			if not link:
				continue
			url = link.text
			if Bing.USER_SUBDOMAIN in url:
				urls.append(url)
		return urls
