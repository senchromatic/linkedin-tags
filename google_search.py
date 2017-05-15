import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://www.google.com/search?q=site%3Alinkedin.com+'
QUERY = '"algorithmic+trader"'
START_NAME = '&start='
USER_SUBDOMAIN = 'linkedin.com/in/'

def get_soup(url):
	html = requests.get(url)
	return BeautifulSoup(html.content, 'lxml') 

def get_profile_urls(query, start):
	start_value = str(start)
	soup = get_soup(BASE_URL + query + START_NAME + start_value)
	results = soup.findAll('div', {'class':'g'})
	urls = []
	for result in results:
		link = result.find('cite')
		url = link.text
		if USER_SUBDOMAIN in url:
			urls.append(url)
	return urls

# urls = get_profile_urls(QUERY, 10)
