from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep


class Utility:
	@staticmethod
	def wait(caller, condition=None):
		if not condition:
			return True
		ready = EC.presence_of_element_located(condition)
		WebDriverWait(caller.browser, caller.MAX_TIMEOUT).until(ready)
		for microsleep in xrange(1, 1+caller.MICROSLEEPS):
			if caller.SCROLL:
				fraction = str(microsleep) + '/' + str(caller.MICROSLEEPS)
				scroll_script = 'window.scrollTo(0, document.body.scrollHeight*' + fraction + ');'
				caller.browser.execute_script(scroll_script)
			sleep(caller.RELOAD_DELAY / caller.MICROSLEEPS)
	
	@staticmethod
	def load(caller, url, condition=None):
		successful = None
		while not successful:
			try:
				caller.browser.get(url)
				Utility.wait(caller, condition)
				successful = True
			except TimeoutException as exception:
				return False
	
	@staticmethod
	def make_soup(caller, url, condition=None):
		Utility.load(caller, url, condition)
		html = caller.browser.page_source
		return BeautifulSoup(html, 'lxml')
	

