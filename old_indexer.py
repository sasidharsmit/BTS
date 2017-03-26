import re
import math
from nltk.stem import PorterStemmer

######################################################## Creating Inverted Index

ps = PorterStemmer()

class Index:

	def __init__(self, files, stopwords):
        	self.filenames = files
		self.stopwords = stopwords
		self.stoplist = self.process_stopwords()
		self.termlist = self.filter_text()
		self.indices = self.make_indices()
		self.index = self.fullIndex()

	def process_stopwords(self):
		file_to_terms = {}
		for file in self.stopwords:
			pattern = re.compile('[\W_]+')
			file_to_terms[file] = open(file, 'r').read().lower();
			file_to_terms[file] = pattern.sub(' ',file_to_terms[file])
			re.sub(r'[\W_]+','', file_to_terms[file])
			file_to_terms[file] = file_to_terms[file].split()
		return file_to_terms

	def diff_list(self,list1,list2):
		difflist = []
		for i in list1:
	    		if i not in list2:
				difflist.append(i)
		return difflist

	def filter_text(self):
		file_to_terms = {}
		for file in self.filenames:
			pattern = re.compile('[\W_]+')
			file_to_terms[file] = open(file, 'r').read().lower();
			file_to_terms[file] = pattern.sub(' ',file_to_terms[file])
			re.sub(r'[\W_]+','', file_to_terms[file])
			file_to_terms[file] = file_to_terms[file].split()
			file_to_terms[file] =self.diff_list(file_to_terms[file],self.stoplist["stopwords.txt"])
			for index in range(len(file_to_terms[file])):
				file_to_terms[file][index] = ps.stem(file_to_terms[file][index])
			file_to_terms[file] = [str(i).strip() for i in file_to_terms[file]]
		return file_to_terms

	def index_one_file(self,termlist):
		fileIndex = {}
		for index, word in enumerate(termlist):
			if word in fileIndex.keys():
				fileIndex[word].append(index)
			else:
				fileIndex[word] = [index]
		return fileIndex

	def make_indices(self):
		total = {}
		for filename in self.termlist.keys():
			total[filename] = self.index_one_file(self.termlist[filename])
		return total

	def fullIndex(self):
		total_index = {}
		for filename in self.indices.keys():
			for word in self.indices[filename].keys():
				if word in total_index.keys():
					if filename in total_index[word].keys():
						print(total_index[word])
						total_index[word][filename].extend(self.indices[filename][word][:])
					else:
						total_index[word][filename] = self.indices[filename][word]
				else:
					total_index[word] = {filename: self.indices[filename][word]}
		return total_index

I = Index({"data/AmazonOrganization1.txt","data/AmazonOrganization2.txt","data/AmazonPlace1.txt","data/AmazonPlace2.txt","data/AmazonPlace3.txt","data/AmazonTransportation1.txt","data/AmazonTransportation2.txt","data/AppleCompany1.txt","data/AppleCompany2.txt","data/AppleFruit2.txt","data/AppleFruit3.txt","data/ApplePlace1.txt","data/ApplePlace2.txt","data/ChipComputing1.txt","data/ChipFilm1.txt","data/ChipFood1.txt","data/EagleBird1.txt","data/EagleMusic1.txt","data/EagleMusic2.txt","data/EagleMusic3.txt","data/EagleVehicle1.txt","data/EagleVehicle2.txt","data/JaguarAnimal1.txt","data/JaguarAnimal2.txt","data/JaguarAnimal3.txt","data/JaguarAutomobile1.txt","data/JaguarAutomobile2.txt","data/JaguarAutomobile3.txt","data/JaguarAutomobile4.txt","data/JaguarScience1.txt","data/JaguarScience2.txt","data/QueenArts1.txt","data/QueenArts2.txt","data/QueenArts3.txt","data/QueenMonarch1.txt","data/QueenMonarch3.txt","data/QueenMusic1.txt","data/QueenMusic2.txt","data/QueenZoology1.txt","data/QueenZoology2.txt","data/QueenMonarch2.txt","QueenMonarch2.txt","data/TabletComputer1.txt","data/TabletComputer2.txt","data/TabletComputer3.txt","data/TabletConfectionery1.txt","data/TabletConfectionery2.txt","data/TabletMedicine1.txt","data/TabletMedicine2.txt","data/TabletWriting1.txt","data/TabletWriting2.txt","data/AppleFruit1.txt"},{"stopwords.txt"})

