from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep


class Utility:
	FALSE_LEADS = ['This profile is not available']
	CAPTCHA_TEXTS = [
		r"Our systems have detected unusual traffic from your computer",
		r"Just a quick security check",
		r"We need to verify you're not a robot! Please complete this security check",
		r"CaptchaV2ChallengeForm",
		r"uas-consumer-captcha-v2"
	]
	
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
	def solve_captcha():
		raw_input('Please solve the captcha and press enter when done')
	
	@staticmethod
	def check_captcha(html):
		if not html:
			return False
		soup = BeautifulSoup(html, 'lxml')
		found_captcha = False
		# method 1: check captcha box
		if soup.find('div', {'id': 'recaptcha'}):
			found_captcha = True
		# method 2: check for text
		for captcha_text in Utility.CAPTCHA_TEXTS:
			if captcha_text in html:
				found_captcha = True
				break
		if found_captcha:
			Utility.solve_captcha()
			return True
		return False
	
	@staticmethod
	def load(caller, url, condition=None):
		Utility.check_captcha(caller.browser.page_source)
		try:
			caller.browser.get(url)
			Utility.wait(caller, condition)
		except TimeoutException as exception:
			Utility.load(caller, url, condition)

	@staticmethod
	def is_false_lead(caller):
		html = caller.browser.page_source
		if not html:
			return False
		for false_lead in Utility.FALSE_LEADS:
			if false_lead in html:
				return True
		return False

	@staticmethod
	def make_soup(caller, url, condition=None):
		Utility.load(caller, url, condition)
		html = caller.browser.page_source
		if Utility.is_false_lead(caller):
			return None
		return BeautifulSoup(html, 'lxml')
