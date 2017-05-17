from getpass import getuser, getpass
from selenium.webdriver.common.by import By
from web_utilities import Utility


class LinkedIn:
	DOMAIN = 'https://www.linkedin.com'
	WELCOME_TEXT = 'Welcome, '
	MAX_TIMEOUT = 10
	RELOAD_DELAY = 5.0
	MICROSLEEPS = 100
	SCROLL = True
	
	def __init__(self, browser):
		self.browser = browser
		self.login()
	
	def login(self):
		print('Please enter your login credentials')
		Utility.load(self, LinkedIn.DOMAIN, (By.PARTIAL_LINK_TEXT, LinkedIn.WELCOME_TEXT))
	
	def download_profile(self, url):
		page = Utility.make_soup(self, url, (By.CLASS_NAME, 'core-rail'))
		profile = page.find('div', {'class' : 'core-rail', 'role' : 'main'})
		return profile

