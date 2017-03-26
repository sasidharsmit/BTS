from querier import *



for string in categoryVec.values():
	split_word_list = []
	queryls = convert_query_to_list(string)
	if queryls[0] == clean_word("jaguar"):
		print(queryls[1])
