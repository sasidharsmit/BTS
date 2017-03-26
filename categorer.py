from scorer import *

categoryVec={'Computing':'tablet computer graphics stylus android','Medicine':'tablet swallow granulation drug','Confectionery':'tablet candy granulation die mixing process milk','Inscription, printing and writing media':'tablet writing century use','Government and Monarchy': 'queen consort succession king regnant empress mother title haley', 'Arts and Literature': 'queen ellery radio magazine station novel', 'Music': 'queen album band club', 'Zoology': 'queen colony virgin bee ant female','Places':'amazon species basin river rainforest creek channel','Organization':'amazon store bookstore company online','Transportation':'amazon engine door yacht volvo','Computing, science and technology':'chip code sequence','Films and Television':'chip officer','Food':'chip potato','Birds':'eagle species prey','Arts and Entertainment':'eagle music film song marcus abba','Vehicles':'eagle drive chrysler brand amc','Fruit':'apple fruit tree red health','Company':'apple company employee campus','Places':'apple population people island boston','Automobile':'jaguar car electric company concept model vehicle design motor','Animal':'jaguar cat animal species predator habitat range forest hunt','Science and Technology':'jaguar system atari console'}

class CategoryCard:

	def __init__(self):
        	self.categorynames = categoryVec
		self.CategoryVectors = self.populate_category_vector()
	
	# Cleaning words	
	
	def clean_word(self, word):
		pattern = re.compile('[\W_]+')
		word = pattern.sub(' ',word)
		word = word.lower()
		word = re.sub('[^0-9a-zA-Z]+','',word)
		word = ps.stem(word)
		return word

	# Convert category string to list

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

	# Category Frequency

	def categoryFreq(self, term, category):
			count = 0
			for word in category.split():
				if word == term:
					count += 1
			return count

	# Term Frequency

	def termfreq_without_filter(self, terms, category):
			categorylist = self.convert_category_to_list(category)
			termslist = terms.split()
			temp = [0]*len(termslist)
			for i,term in enumerate(termslist):
				temp[i] = self.categoryFreq(term, ' '.join(categorylist))
			return temp
	
	# Category TF-IDF vector

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

	# Populate CategoryCard

	def populate_category_vector(self):
			vecs = {}
			for key in self.categorynames.keys():
					vecs[key] = self.category_vec(self.categorynames[key])
			return vecs

C = CategoryCard()

