from bs4 import BeautifulSoup
from getpass import getuser, getpass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep


class LinkedIn:
	DOMAIN = 'https://www.linkedin.com'
	WELCOME_TEXT = 'Welcome, '
	MAX_TIMEOUT = 60
	SAFE_DELAY = 5.0
	MICROSLEEPS = 10
	
	def __init__(self):
		self.browser = webdriver.Firefox()
		self.login()
	
	def wait(self, condition, scroll=False):
		if not condition:
			return
		ready = EC.presence_of_element_located(condition)
		WebDriverWait(self.browser, LinkedIn.MAX_TIMEOUT).until(ready)
		for microsleep in xrange(1, 1+LinkedIn.MICROSLEEPS):
			if scroll:
				fraction = str(microsleep) + '/' + str(LinkedIn.MICROSLEEPS)
				scroll_script = 'window.scrollTo(0, document.body.scrollHeight*' + fraction + ');'
				self.browser.execute_script(scroll_script)
			sleep(LinkedIn.SAFE_DELAY / LinkedIn.MICROSLEEPS)
	
	def load(self, url, condition=None, scroll=False):
		self.browser.get(url)
		self.wait(condition, scroll)
	
	def make_soup(self, url, condition=None, scroll=False):
		self.load(url, condition, scroll)
		html = self.browser.page_source
		return BeautifulSoup(html, 'lxml')
	
	def login(self):
		print('Please enter your login credentials')
		self.load(LinkedIn.DOMAIN, (By.PARTIAL_LINK_TEXT, LinkedIn.WELCOME_TEXT))
	
	def download_profile(self, url):
		page = self.make_soup(url, (By.CLASS_NAME, 'core-rail'), True)
		profile = page.find('div', {'class' : 'core-rail', 'role' : 'main'})
		return profile


