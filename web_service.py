from bs4 import BeautifulSoup
from getpass import getuser, getpass
import requests


class LinkedIn:
	USERNAME_PROMPT = 'LinkedIn username [e.g. winston_smith1944@minimail.com]: '
	DOMAIN = 'https://www.linkedin.com'
	LOGIN_URL = 'https://www.linkedin.com/uas/login-submit'
	
	def __init__(self):
		self.client = requests.Session()
		self.prompt_credentials()
		self.login()
	
	def prompt_credentials(self):
		self.username = getpass(LinkedIn.USERNAME_PROMPT)
		self.password = getpass()
	
	def get_soup(self, url):
		html = self.client.get(url).content
		return BeautifulSoup(html, 'lxml')
	
	def login(self):
		soup = self.get_soup(LinkedIn.DOMAIN)
		csrf = soup.find(id="loginCsrfParam-login")['value']
		login_information = {
    		'session_key':self.username,
    		'session_password':self.password,
    		'loginCsrfParam': csrf,
		}
		self.client.post(LinkedIn.LOGIN_URL, data=login_information)
