from information_retrieval import Retriever

def prompt(retriever):
	retriever.query = raw_input('Please query an occupational role, e.g. "software+engineer": ')
	return retriever.query

if __name__ == '__main__':
	retriever = Retriever()
	while prompt(retriever):
		retriever.download_all_data()
