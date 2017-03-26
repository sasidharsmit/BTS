from indexer import *

import math

class ScoreCard:
	
	def __init__(self):
        	self.filenames = I.filenames
		self.vectors = self.vectorize()
		self.mags = self.magnitudes()
		self.ScoreVectors = self.populate_scores_vector()

	#Document Frequency

	def document_frequency(self, term):
		if term in I.index.keys():
			return len(I.index[term].keys()) 
		else:
			return 0

	#Collection size

	def collection_size(self):
		return len(I.filenames)

	#Vectorize

	def vectorize(self):
		vectors = {}
		for filename in I.filenames:
			vectors[filename] = [len(I.indices[filename])]
		return vectors		

	#Size of Documents

	def magnitudes(self):
			mags = {}
			for document in I.filenames:
				mags[document] = pow(sum(map(lambda x: x**2, self.vectors[document])),.5)
			return mags

	#Term Count in document

	def number_of_terms(self, term, document):
		if term in I.termlist[document]:
			return len(I.index[term][document])
		else:
			return 0

	#Term Frequency

	def term_frequency(self, term, document):
		return self.number_of_terms(term,document)/self.mags[document]

	#Inverse Document Frequency Equation

	def idf_function(self, N, N_t):
		if N_t != 0:
			return math.log(N/1+N_t) #Check about smoothing: could be N/1+N_t
		else:
			return 0

	#Inverse Document Frequency

	def inverse_document_frequency(self, term):
		TotalDoc = self.collection_size()
		DocFreq = self.document_frequency(term)
		return self.idf_function(TotalDoc,DocFreq)

	#Generate score for each term in document

	def generateScore(self, term, document):
		return self.term_frequency(term,document) * self.inverse_document_frequency(term)

	#Populate ScoreCard

	def populate_scores_vector(self):
			vecs = {}
			for doc in I.filenames:
				docVec = [0]*len(I.index.keys())
				for ind, term in enumerate(I.index.keys()):
					docVec[ind] = round(self.generateScore(term, doc),4)
				vecs[doc] = docVec
			return vecs

S = ScoreCard()

