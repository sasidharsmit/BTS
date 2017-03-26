from scorer import *

categoryVec={'Fruit': 'apple fruit red', 'Company': 'apple company computer', 'Animal': 'jaguar leopard cat', 'Car': 'jaguar car company'}

class CategoryCard:

	def __init__(self):
        	self.categorynames = categoryVec
		self.CategoryVectors = self.populate_category_vector()

	def clean_word(self, word):
		pattern = re.compile('[\W_]+')
		word = pattern.sub(' ',word)
		word = word.lower()
		word = re.sub('[^0-9a-zA-Z]+','',word)
		word = ps.stem(word)
		return word

	def convert_category_to_list(self, string):
		pattern = re.compile('[\W_]+')
		string = pattern.sub(' ',string)
		categorylist = []
		for word in string.split():	
			word = self.clean_word(word)
			categorylist.append(word)
		categorylist = I.diff_list(categorylist,I.stoplist)
		categorylist = [str(i).strip() for i in categorylist]
		return categorylist

	def categoryFreq(self, term, category):
			count = 0
			for word in category.split():
				if word == term:
					count += 1
			return count

	def termfreq_without_filter(self, terms, category):
			categorylist = self.convert_category_to_list(category)
			termslist = terms.split()
			temp = [0]*len(termslist)
			for i,term in enumerate(termslist):
				temp[i] = self.categoryFreq(term, ' '.join(categorylist))
			return temp

	def category_vec(self, category):
			categoryls = self.convert_category_to_list(category)
			categoryVec = [0]*len(categoryls)
			index = 0
			for ind, word in enumerate(categoryls):
				categoryVec[index] = self.categoryFreq(word, ' '.join(categoryls)) 
				index += 1
			categoryidf = [S.inverse_document_frequency(word) for word in I.index.keys()]
			ZeroList = listofzeros = [0.0] * len(categoryVec)
			if categoryVec == ZeroList:
				return [0.0] * len(I.index.keys())
			else:
				magnitude = pow(sum(map(lambda x: x**2, categoryVec)),.5)
				freq = self.termfreq_without_filter(' '.join(I.index.keys()), category)
				tf = [x/magnitude for x in freq]
				final = [round(tf[i]*categoryidf[i],4) for i in range(len(I.index.keys()))]
				return final

	def generateCategoryScore(self, term, document):
		return self.term_frequency(term,document) * self.inverse_document_frequency(term)

	def populate_category_vector(self):
			vecs = {}
			for key in self.categorynames.keys():
					vecs[key] = self.category_vec(self.categorynames[key])
			return vecs

C = CategoryCard()

