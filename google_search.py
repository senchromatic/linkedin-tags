from bs4 import BeautifulSoup
from datetime import datetime
from document_manager import Database
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep


class Google:
	BASE_URL = 'https://www.google.com/search?q=site%3Alinkedin.com/in+'
	START_NAME = '&start='
	USER_SUBDOMAIN = 'linkedin.com/in/'
	MAX_TIMEOUT = 60
	SAFE_DELAY = 5.0
	
	def __init__(self, browser):
		self.last_visit = None
		self.browser = browser
	
	def wait(self):
		ready = EC.presence_of_element_located((By.CLASS_NAME, 'g'))
		try:
			WebDriverWait(self.browser, Google.MAX_TIMEOUT).until(ready)
			sleep(Google.SAFE_DELAY)
			return True
		except TimeoutException as exception:
			return False		
	
	def load(self, url):
		successful = None
		while not successful:
			self.browser.get(url)
			successful = self.wait()
	
	def make_soup(self, url):
		self.load(url)
		html = self.browser.page_source
		return BeautifulSoup(html, 'lxml')
	
	def get_profile_urls(self, query, start):
		if self.last_visit:
			time_difference = datetime.now() - self.last_visit
			remaining = max(0, Google.SAFE_DELAY - time_difference.total_seconds())
			sleep(remaining)
		self.last_visit = datetime.now()
		start_value = str(start)
		soup = self.make_soup(Google.BASE_URL + query + Google.START_NAME + start_value)
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
