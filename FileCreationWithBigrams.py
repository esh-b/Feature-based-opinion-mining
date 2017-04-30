import re
import nltk
import string
import enchant
import operator
from nltk.corpus import stopwords
from collections import OrderedDict 
from textblob import TextBlob, Word
from textblob import Blobber
from textblob.taggers import NLTKTagger

apostropheList = {"n't" : "not","aren't" : "are not","can't" : "cannot","couldn't" : "could not","didn't" : "did not","doesn't" : "does not", \
				  "don't" : "do not","hadn't" : "had not","hasn't" : "has not","haven't" : "have not","he'd" : "he had","he'll" : "he will", \
				  "he's" : "he is","I'd" : "I had","I'll" : "I will","I'm" : "I am","I've" : "I have","isn't" : "is not","it's" : \
				  "it is","let's" : "let us","mustn't" : "must not","shan't" : "shall not","she'd" : "she had","she'll" : "she will", \
				  "she's" : "she is", "shouldn't" : "should not","that's" : "that is","there's" : "there is","they'd" : "they had", \
				  "they'll" : "they will", "they're" : "they are","they've" : "they have","we'd" : "we had","we're" : "we are","we've" : "we have", \
				  "weren't" : "were not", "what'll" : "what will","what're" : "what are","what's" : "what is","what've" : "what have", \
				  "where's" : "where is","who'd" : "who had", "who'll" : "who will","who're" : "who are","who's" : "who is","who've" : "who have", \
				  "won't" : "will not","wouldn't" : "would not", "you'd" : "you had","you'll" : "you will","you're" : "you are","you've" : "you have"}
				  
stopWords = stopwords.words("english")
exclude = set(string.punctuation)
exclude.remove("_")
linkPtrn = re.compile("^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$")

#English vocabulary
enchVocab = enchant.Dict("en_US")
vocabList = set(w.lower() for w in nltk.corpus.words.words())

def fileCreation(reviewContent,filename):
	phrasesDict = dict()

	for a in range(len(reviewContent)):								#Stores the score of the nouns
		for i in range(len(reviewContent[a])):
			line_words = reviewContent[a][i]
			#line_words = str(TextBlob(line_words).correct())
			#line_words = ' '.join(TextBlob(line_words).words)
			#if 'room' in line_words:
			#	line_words = re.sub('room', 'zoom', line_words)

			phrases = TextBlob(line_words).noun_phrases
			for p in phrases:
				if(len(p.split()) == 2):
					if(p not in phrasesDict):
						phrasesDict[p] = 1
					else:
						phrasesDict[p] += 1

	
	filterAdj(phrasesDict,filename)

def filterAdj(phrasesDict,filename):
	phrasesDict = OrderedDict(sorted(phrasesDict.items(), key=operator.itemgetter(1), reverse=True))
	newPhrases = dict()
	exclude = set(string.punctuation)
	exclude.remove("_")
	for line_words, count in phrasesDict.items():
		line_words = ' '.join([apostropheList[word] if word in apostropheList else word for word in line_words.split()])
		line_words = ''.join(ch for ch in line_words if ch not in exclude)
		line_words = re.sub(r' [a-z][$]? ', ' ', line_words)
		line_words = [Word(word).lemmatize() for word in line_words.split() if(word not in stopwords.words("english") and not word.isdigit()) and len(word) > 2]
		line_words = ' '.join(line_words)
		if(len(line_words.strip(" ").split()) == 2):
			if(line_words in newPhrases):
				newPhrases[line_words] += count
			else:
				newPhrases[line_words] = count
	#Bigrams from the file
	newPhrases = OrderedDict(sorted(newPhrases.items(), key=operator.itemgetter(1), reverse=True))

	#Applying Threshold to Bigrams
	nouns1 = []
	for key, value in newPhrases.items():
		if value >= 3:
			nouns1.append(key)
			print key


	stopWords = stopwords.words("english")
	exclude = set(string.punctuation)
	reviewTitle = []
	reviewContent = []

	#Reading the original file
	with open(filename) as f:
		review = []
		for line in f:
			if line[:3] == "[t]":
				if review:
					reviewContent.append(review)
					review = []
				reviewTitle.append(line.split("[t]")[1].rstrip("\r\n"))
			else:
				if "##" in line:
					x = line.split("##")
					#if len(x[0]) != 0:
					for i in xrange(1, len(x)):
						review.append(x[i].rstrip("\r\n"))
				else:
					continue
		reviewContent.append(review)

		#tb = Blobber(pos_tagger=PerceptronTagger()) 
		tb = Blobber(pos_tagger=NLTKTagger())
		nounScores = dict()

		#Writing to a file
		f = open('modified.txt', 'w')
		for a in xrange(len(reviewContent)):
			f.write("[t]")
			
			#Finding Bigrams in title
			text = reviewTitle[a]
		
			x = tb(text).tags #NLTK tagger		
			e = 0
				
			while e<len(x):
				tagList = ""
				temp = ""
				wrt = x[e][0]
				#f.write(x[e][0])
				e = e+1
				count = e
				tp = 0
				if(count<len(x) and (x[count-1][1] == "NN" or "JJ") and (x[count][1] == "NN" or "JJ")):
					tagList = x[count-1][0] + " " + x[count][0]
					temp = x[count][0]
					count = count+1
				if tagList != "":
					if tagList in nouns1: 
						tagList = tagList.replace(' ', '')
						f.write(tagList)
						tp = 1
						e = count
				if tp == 0:
					f.write(wrt)
				f.write(" ")			


			f.write("\r\n")	
								
			#Finding bigrams in review
			for i in xrange(len(reviewContent[a])):
				text = reviewContent[a][i]
				x = tb(text).tags #NLTK tagger
				
				tagList = []
				e = 0
				f.write("##")
				"""
				while e<len(x):
					tagList = []
					f.write(x[e][0])
					e = e+1
					count = e
					if(count<len(x) and x[count-1][1] == "NN" and x[count][1] == "NN"):
						tagList.append(x[count-1][0])
				
						while(count < len(x) and x[count][1] == "NN"):
							tagList.append(x[count][0])
							count = count+1
					if tagList != []:
						if set(tagList) <= nouns: 
							print tagList
					
							for t in range(1,len(tagList)):
								f.write("_"+tagList[t])
							e = count
					f.write(" ")
				f.write(".\r\n")
				"""
				while e<len(x):
					tagList = ""
					temp = ""
					wrt = x[e][0]
					#f.write(x[e][0])
					e = e+1
					count = e
					tp = 0
					if(count<len(x) and (x[count-1][1] == "NN" or "JJ") and (x[count][1] == "NN" or "JJ")):
						tagList = x[count-1][0] + " " + x[count][0]
						temp = x[count][0]
						count = count+1
					if tagList != "":
						#Checking if consecutive nouns we found out are in noun phrases
						if tagList in nouns1: 
							#print tagList
							#Removing space between words in a bigram
							tagList = tagList.replace(' ', '')
							f.write(tagList)
							tp = 1
							e = count
					if tp == 0:
						f.write(wrt)
					f.write(" ")
				f.write(".\r\n")
		

		
	
