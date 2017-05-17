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
		# temp (backup)
		normal_scroll = LinkedIn.SCROLL
		normal_delay = LinkedIn.RELOAD_DELAY
		LinkedIn.SCROLL = False
		LinkedIn.RELOAD_DELAY = 0.0
		Utility.load(self, LinkedIn.DOMAIN, (By.PARTIAL_LINK_TEXT, LinkedIn.WELCOME_TEXT))
		# restore
		LinkedIn.SCROLL = normal_scroll
		LinkedIn.RELOAD_DELAY = normal_delay
	
	def download_profile(self, url):
		page = Utility.make_soup(self, url, (By.CLASS_NAME, 'core-rail'))
		if not page:
			return page
		profile = page.find('div', {'class' : 'core-rail', 'role' : 'main'})
		return profile

