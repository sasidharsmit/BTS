import re
import math
import string
from nltk.stem import PorterStemmer
from scipy import spatial

######################################################## Creating Inverted Index

ps = PorterStemmer()

def process_stopwords(filenames):
	file_to_terms = {}
	for file in filenames:
		pattern = re.compile('[\W_]+')
		file_to_terms[file] = open(file, 'r').read().lower();
		file_to_terms[file] = pattern.sub(' ',file_to_terms[file])
		re.sub(r'[\W_]+','', file_to_terms[file])
		file_to_terms[file] = file_to_terms[file].split()
	return file_to_terms

stoplist = process_stopwords({"stopwords.txt"})

def diff_list(list1,list2):
	difflist = []
	for i in list1:
    		if i not in list2:
        		difflist.append(i)
	return difflist

def filter_text(filenames):
	file_to_terms = {}
	for file in filenames:
		pattern = re.compile('[\W_]+')
		file_to_terms[file] = open(file, 'r').read().lower();
		file_to_terms[file] = pattern.sub(' ',file_to_terms[file])
		re.sub(r'[\W_]+','', file_to_terms[file])
		file_to_terms[file] = file_to_terms[file].split()
		file_to_terms[file] = diff_list(file_to_terms[file],stoplist["stopwords.txt"])
		for index in range(len(file_to_terms[file])):
			file_to_terms[file][index] = ps.stem(file_to_terms[file][index])
		file_to_terms[file] = [str(i).strip() for i in file_to_terms[file]]
	return file_to_terms

def index_one_file(termlist):
	fileIndex = {}
	for index, word in enumerate(termlist):
		if word in fileIndex.keys():
			fileIndex[word].append(index)
		else:
			fileIndex[word] = [index]
	return fileIndex

def make_indices(termlists):
	total = {}
	for filename in termlists.keys():
		total[filename] = index_one_file(termlists[filename])
	return total

def fullIndex(regdex):
	total_index = {}
	for filename in regdex.keys():
		for word in regdex[filename].keys():
			if word in total_index.keys():
				if filename in total_index[word].keys():
					print(total_index[word])
					total_index[word][filename].extend(regdex[filename][word][:])
				else:
					total_index[word][filename] = regdex[filename][word]
			else:
				total_index[word] = {filename: regdex[filename][word]}
	return total_index

filenames = {"text.txt","testfile.txt","top.txt","tell.txt"} #"jaguarcat.txt","jaguarcars.txt"

termlist = filter_text(filenames)
#print(termlist)
indices = make_indices(termlist)
#print(indices)
FullIndex = fullIndex(indices)
	
#print(FullIndex) 

######################################################### Creating Score Card

#Document Frequency

def document_frequency(term):
		if term in FullIndex.keys():
			return len(FullIndex[term].keys()) 
		else:
			return 0

#Collection size

def collection_size(filenames):
	return len(filenames)

def regIndex(filenames):
	return make_indices(filter_text(filenames))

#Vectorize

def vectorize(filenames):
	vectors = {}
	for filename in filenames:
		filename1 = set([filename])
		vectors[filename] = [len(regIndex(filename1)[word]) for word in regIndex(filename1).keys()]
	return vectors		

#Size of Documents

def magnitudes(documents):
		mags = {}
		for document in documents:
			document1 = set([document])
			vectors = vectorize(document1)
			mags[document] = pow(sum(map(lambda x: x**2, vectors[document])),.5)
		return mags

#Term Count in document

def number_of_terms(term,document):
	if term in termlist[document]:
		return len(FullIndex[term][document])
	else:
		return 0

#Term Frequency

def term_frequency(term, document):
	document1 = set([document])
	mags = magnitudes(document1)
	return number_of_terms(term,document)/mags[document]

#Inverse Document Frequency Equation

def idf_function(N,N_t):
	if N_t != 0:
		return math.log(N/1+N_t) #Check about smoothing: could be N/1+N_t
	else:
		return 0

#Inverse Document Frequency

def inverse_document_frequency(term):
	TotalDoc = collection_size(filenames)
	DocFreq = document_frequency(term)
	return idf_function(TotalDoc,DocFreq)

#Generate score for each term in document

def generateScore(term, document):
	return term_frequency(term,document) * inverse_document_frequency(term)

#Populate ScoreCard

def populate_scores_vector(documents):
		vecs = {}
		for doc in documents:
			docVec = [0]*len(FullIndex.keys())
			for ind, term in enumerate(FullIndex.keys()):
				docVec[ind] = round(generateScore(term, doc),4)
			vecs[doc] = docVec
		return vecs

ScoreCard = populate_scores_vector(filenames)

############################################################## Querying

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
		result += one_word_query(word,FullIndex)
	return list(set(result))

def phrase_query(string, invertedIndex):
	listword = []
	pattern = re.compile('[\W_]+')
	string = pattern.sub(' ',string)
	listOfLists, result = [],[]
	for word in string.split():
		word = clean_word(word)
		listword.append(word)
	listword = diff_list(listword,stoplist["stopwords.txt"])
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
	querylist = diff_list(querylist,stoplist["stopwords.txt"])
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

#print(queryFreq("oz","the wizard of Oz"))

#print(termfreq("martha's red CAR","Martha's car is red"))

def query_vec(query):
		queryls = convert_query_to_list(query)
		queryVec = [0]*len(queryls)
		index = 0
		for ind, word in enumerate(queryls):
			queryVec[index] = queryFreq(word, query)
			index += 1
		
		queryidf = [inverse_document_frequency(word) for word in FullIndex.keys()]
		
		ZeroList = listofzeros = [0.0] * len(queryVec)
		if queryVec == ZeroList:
			return [0.0] * len(FullIndex.keys())
		else:
			magnitude = pow(sum(map(lambda x: x**2, queryVec)),.5)
			freq = termfreq_without_filter(' '.join(FullIndex.keys()), query)
			tf = [x/magnitude for x in freq]
			final = [round(tf[i]*queryidf[i],4) for i in range(len(FullIndex.keys()))]
			return final

def cosine_similarity(documentvec, queryvec):
	return round(1 - spatial.distance.cosine(documentvec, queryvec),4)

def retrieve_results(results, queryvec):
	CosineDict = {}
	for filename in results:
		CosineDict[filename] = cosine_similarity(ScoreCard[filename], queryvec)
	return CosineDict

########################################################### Ranking Results


	
#print(sorted(RankedDocuments.values(), reverse=True))
#print(sorted(RankedDocuments.items(), key = lambda x:x[1],reverse=True))

def present_ranked_documents(documentlist):
	for i in range(0,len(documentlist)):
		print(documentlist[i])
	return 0

########################################################### Search Engine

def intersection_list(list1,list2):
	inter = set(list1).intersection(set(list2))
	inter = list(inter)
	return inter

def search_engine_no_split(query):
	QueryResults = free_text_query(query)
	QueryVector = query_vec(query)
	RetrievedResults = retrieve_results(QueryResults, QueryVector)
	print(RetrievedResults)
	RankedDocumentsSorted = sorted(RetrievedResults,key=RetrievedResults.get, reverse=True)
	RankedDocumentsSorted = RankedDocumentsSorted[:10]
	present_ranked_documents(RankedDocumentsSorted)
	return None

def search_engine(query):
	QueryResults = free_text_query(query)
	QueryVector = query_vec(query)
	RetrievedResults = retrieve_results(QueryResults, QueryVector)
	listA = FullIndex["sweet"].keys()
	listB = FullIndex["fileand"].keys()
	interA_R = intersection_list(RetrievedResults,listA)
	interB_R = intersection_list(RetrievedResults,listB)
	interlistAsorted = sorted(interA_R,key=RetrievedResults.get, reverse=True)
	interlistBsorted = sorted(interB_R,key=RetrievedResults.get, reverse=True)
	interlistAsorted = interlistAsorted[:5]
	interlistBsorted = interlistBsorted[:5]
	return interlistAsorted, interlistBsorted

#results = search_engine("wizard")

#print(results[0])

#present_ranked_documents(results[0])

#print(results[1])

#present_ranked_documents(results[1])

##########################################################
print("\n\n")

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
				CosineDocVec[filename1,filename2] = cosine_similarity(ScoreCard[filename1],ScoreCard[filename2])
	return CosineDocVec

#print(ScoreCard)
CosineDocValues = document_cosine_value(filenames)


def find_different_documents():
	for term in CosineDocValues.keys():
		if CosineDocValues[term] < 0.1 and CosineDocValues[term] >-0.1:
			return term
			break

print(find_different_documents())

print("\n\n")




