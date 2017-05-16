from document_manager import Database


class Google:
	BASE_URL = 'https://www.google.com/search?q=site%3Alinkedin.com+'
	START_NAME = '&start='
	USER_SUBDOMAIN = 'linkedin.com/in/'

	@staticmethod	
	def get_profile_urls(query, start):
		start_value = str(start)
		soup = Database.download_dom(Google.BASE_URL + query + Google.START_NAME + start_value)
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
