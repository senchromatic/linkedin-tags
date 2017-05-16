from information_retrieval import Retriever

if __name__ == "__main__":
	query = raw_input('"lorem+ipsum"\n')
	retriever = Retriever(query)
	retriever.download_all_data()
