from categorer import *
from scipy import spatial

# Cleaning words

def clean_word(word):
	pattern = re.compile('[\W_]+')
	word = pattern.sub(' ',word)
	word = word.lower()
	word = re.sub('[^0-9a-zA-Z]+','',word)
	word = ps.stem(word)
	return word

#One Word Query

def one_word_query(word, invertedIndex):
	word = clean_word(word)
	if word in invertedIndex.keys():
		return [filename for filename in invertedIndex[word].keys()]
	else:
		return []

# Two or more Word Query

def free_text_query(string):
	pattern = re.compile('[\W_]+')
	string = pattern.sub(' ',string)
	result = []
	for word in string.split():
		result += one_word_query(word,I.index)
	return list(set(result))

def phrase_query(string, invertedIndex):
	listword = []
	pattern = re.compile('[\W_]+')
	string = pattern.sub(' ',string)
	listOfLists, result = [],[]
	for word in string.split():
		word = clean_word(word)
		listword.append(word)
	listword = I.diff_list(listword,I.stoplist)
	for word in listword:	
		listOfLists.append(one_word_query(word,invertedIndex))
	setted = set(listOfLists[0]).intersection(*listOfLists)
	for filename in setted:
		temp = []
		for word in listword:
			temp.append(invertedIndex[word][filename][:])
		for i in range(len(temp)):
			for ind in range(len(temp[i])):
				temp[i][ind] -= i
		if set(temp[0]).intersection(*temp):
			result.append(filename)
	return result

# Convert query string to list

def convert_query_to_list(string):
	pattern = re.compile('[\W_]+')
	string = pattern.sub(' ',string)
	querylist = []
	for word in string.split():	
		word = clean_word(word)
		querylist.append(word)
	querylist = I.diff_list(querylist,I.stoplist)
	querylist = [str(i).strip() for i in querylist]
	return querylist	

def queryFreq(term, query):
		count = 0
		for word in query.split():
			if word == term:
				count += 1
		return count

def termfreq(terms, query):
		querylist = convert_query_to_list(query)
		termslist = convert_query_to_list(terms)
		temp = [0]*len(termslist)
		for i,term in enumerate(termslist):
			temp[i] = queryFreq(term, ' '.join(querylist))
		return temp

def termfreq_without_filter(terms, query):
		querylist = convert_query_to_list(query)
		termslist = terms.split()
		temp = [0]*len(termslist)
		for i,term in enumerate(termslist):
			temp[i] = queryFreq(term, ' '.join(querylist))
		return temp

def term_frequency(term, document):
	document1 = set([document])
	mags = magnitudes(document1)
	return number_of_terms(term,document)/mags[document]

def query_vec(query):
		queryls = convert_query_to_list(query)
		queryVec = [0]*len(queryls)
		index = 0
		for ind, word in enumerate(queryls):
			queryVec[index] = queryFreq(word, ' '.join(queryls)) 
			index += 1
		queryidf = [S.inverse_document_frequency(word) for word in I.index.keys()]
		ZeroList = listofzeros = [0.0] * len(queryVec)
		if queryVec == ZeroList:
			return [0.0] * len(I.index.keys())
		else:
			magnitude = pow(sum(map(lambda x: x**2, queryVec)),.5)
			freq = termfreq_without_filter(' '.join(I.index.keys()), query)
			tf = [x/magnitude for x in freq]
			final = [round(tf[i]*queryidf[i],4) for i in range(len(I.index.keys()))]
			return final

def cosine_similarity(documentvec, queryvec):
	return round(1 - spatial.distance.cosine(documentvec, queryvec),4)

def retrieve_results(results, queryvec):
	CosineDict = {}
	for filename in results:
		CosineDict[filename] = cosine_similarity(S.ScoreVectors[filename], queryvec)
	return CosineDict

########################################################### Ranking Results


	
#print(sorted(RankedDocuments.values(), reverse=True))
#print(sorted(RankedDocuments.items(), key = lambda x:x[1],reverse=True))

def present_ranked_documents(documentlist):
	for i in range(0,len(documentlist)):
		print(documentlist[i])
	return 0

########################################################### Search Engine


def search_engine_1(query,RankedDocumentsSorted):
	QueryResults = free_text_query(query)
	QueryVector = query_vec(query)
	RetrievedResults = retrieve_results(QueryResults, QueryVector)
	print(RetrievedResults)
	RankedDocumentsSorted = sorted(RetrievedResults,key=RetrievedResults.get, reverse=True)
	RankedDocumentsSorted = RankedDocumentsSorted[:10]
	present_ranked_documents(RankedDocumentsSorted)
	return RankedDocumentsSorted




#search_engine_1("apple")






########################################### Ignore everything below this line: Work in Progress ############################################












#print(query_vec("apple fruit red"))

#search_engine_1("apple")


#Quv = query_vec("apple fruit red")

#print(retrieve_results())


#search_engine_1("apple company technology computer")


#print(C.CategoryVectors)


def intersection_list(list1,list2):
	inter = set(list1).intersection(set(list2))
	inter = list(inter)
	return inter

def intersection_lists(list1, list2, list3):
	inter = set(list1) & set(list2) & set(list3)
	inter = list(inter)
	return inter

def search_engine_2(query):
	QueryResults = free_text_query(query)
	QueryVector = query_vec(query)
	RetrievedResults = retrieve_results(QueryResults, QueryVector)
	listA = I.index[clean_word("company")].keys()
	listB = I.index[clean_word("fruit")].keys()
	#listC = I.index[clean_word("computer")].keys()
	#listD = I.index[clean_word("tree")].keys()
	interA_R = intersection_list(RetrievedResults,listA)
	interB_R = intersection_list(RetrievedResults,listB)
	#interA_R = intersection_lists(RetrievedResults,listA,listC)
	#interB_R = intersection_lists(RetrievedResults,listB,listD)
	interlistAsorted = sorted(interA_R,key=RetrievedResults.get, reverse=True)
	interlistBsorted = sorted(interB_R,key=RetrievedResults.get, reverse=True)
	interlistAsorted = interlistAsorted[:5]
	interlistBsorted = interlistBsorted[:5]
	return interlistAsorted, interlistBsorted


##################################################################################

def search_engine_3(query):
	QueryResults = free_text_query(query)
	QueryVector = query_vec(query)
	RetrievedResults = retrieve_results(QueryResults, QueryVector)
	listA = I.index[clean_word("company")].keys()
	listB = I.index[clean_word("fruit")].keys()
	#listC = I.index[clean_word("computer")].keys()
	#listD = I.index[clean_word("tree")].keys()
	interA_R = intersection_list(RetrievedResults,listA)
	interB_R = intersection_list(RetrievedResults,listB)
	#interA_R = intersection_lists(RetrievedResults,listA,listC)
	#interB_R = intersection_lists(RetrievedResults,listB,listD)
	interlistAsorted = sorted(interA_R,key=RetrievedResults.get, reverse=True)
	interlistBsorted = sorted(interB_R,key=RetrievedResults.get, reverse=True)
	interlistAsorted = interlistAsorted[:5]
	interlistBsorted = interlistBsorted[:5]
	return interlistAsorted, interlistBsorted


#print(categoryVec.values()[0])


#print(search_engine_2("apple"))


#print(results[0])

#present_ranked_documents(results[0])

#print(results[1])

#present_ranked_documents(results[1])

##########################################################



























#print("\n\n")

def word_count(filename):
	WordCount = {}
	for term in indices[filename].keys():
		WordCount[term] = len(indices[filename][term])
	return WordCount

def retrieve_second_highest_word(filename):
	WordCount1 = word_count(filename)
	ValueList1 = WordCount1.values()
	ValueList1.remove(max(ValueList1))
	for term in WordCount1.keys():
		if WordCount1[term] == max(ValueList1):
			return term

#retrieve_second_highest_word(filename)
#retrieve_second_highest_word(filename)
	
#print(retrieve_second_highest_word("jaguarcars.txt"))
def document_cosine_value(filenames):
	CosineDocVec = {}
	for filename1 in filenames:
		for filename2 in filenames:
			if filename1 != filename2:
				CosineDocVec[filename1,filename2] = cosine_similarity(S.ScoreVectors[filename1],S.ScoreVectors[filename2])
	return CosineDocVec

#print(S.ScoreVectors)
#CosineDocValues = document_cosine_value(I.filenames)


def find_different_documents():
	for term in CosineDocValues.keys():
		if CosineDocValues[term] < 0.1 and CosineDocValues[term] >-0.1:
			return term
			break

#print(find_different_documents())
#print(I.index)
#print("\n\n")




