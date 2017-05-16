from information_retrieval import Retriever

MAX_PAGES = 1000
FAILSAFE_THRESHOLD = 10
QUERY = '"algorithmic+trader"'

retriever = Retriever()
retriever.query = QUERY
consecutive_fails = 0
for page in xrange(MAX_PAGES):
	print('Downloading page ' + str(page))
	if retriever.download(page):
		consecutive_fails = 0
	else:
		consecutive_fails += 1
	if consecutive_fails > FAILSAFE_THRESHOLD:
		print('Unable to find more profiles')
		break
