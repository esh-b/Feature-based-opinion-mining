import re
import nltk
import string
import enchant
import operator
from nltk.corpus import stopwords
from collections import OrderedDict 
from textblob import TextBlob, Word

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

#Max hops to find the nearby noun from the position of adjective
maxHops = 4

def findFeatures(reviewContent):
	nounScores = dict()
	adjDict = dict()
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

			line_words = ' '.join([apostropheList[word] if word in apostropheList else word for word in line_words.split()])

			line_words = re.sub(linkPtrn, '', line_words)
			line_words = ''.join(ch for ch in line_words if ch not in exclude)
			line_words = re.sub(r' [a-z][$]? ', ' ', line_words)

			line_words = [Word(word).lemmatize() for word in line_words.split() if(word not in stopwords.words("english") and not word.isdigit()) and len(word) > 2]
			line_words = ' '.join(line_words)

			line_words = nltk.word_tokenize(line_words)
			x = nltk.pos_tag(line_words)
			#x = TextBlob(line_words).tags #textblob tagger
			#x = tb(text).tags #Perceptron tagger 

			#Get the noun/adjective words and store it in tagList
			tagList = []

			for e in x:
				if(e[1] == "NN" or e[1] == "JJ"):
					tagList.append(e)
		
			tagList = list(x)
			#Add the nouns(which are not in the nounScores dict) to the dict
			for e in tagList:
				if "NN" in e[1]:
					if e[0] not in nounScores:
						nounScores[e[0]] = 0

			#For every adjective, find nearby noun
			for l in range(len(tagList)):
				if("JJ" in tagList[l][1]):
					j = k = leftHop = rightHop = -1
					
					#Find the closest noun to the right of the adjective in the line
					for j in range(l + 1, len(tagList)):
						if(j == l + maxHops):
							break
						if("NN" in tagList[j][1]):
							rightHop = (j - l)
							break

					#Find the closest noun to the left of the adjective in the line
					for k in range(l - 1, -1, -1):
						#Incase hopped the 'maxHops' number of words and no noun was found, ignore the adjective
						if(j == l - maxHops):
							break
						if("NN" in tagList[k][1]):
							leftHop = (l - k)
							break

					#Compare which noun is closer to adjective(left or right) and assign the adj to corresponding noun
					if(leftHop > 0 and rightHop > 0):					#If nouns exist on both sides of adjective
						if (leftHop - rightHop) >= 0:						#If left noun is farther
							adjDict[tagList[l][0]] = tagList[j][0]
							nounScores[tagList[j][0]] += 1
						else:														#If right noun is farther
							adjDict[tagList[l][0]] = tagList[k][0]
							nounScores[tagList[k][0]] += 1
					elif leftHop > 0:											#If noun is not found on RHS of adjective
						adjDict[tagList[l][0]] = tagList[k][0]
						nounScores[tagList[k][0]] += 1
					elif rightHop > 0:										#If noun is not found on LHS of adjective
						adjDict[tagList[l][0]] = tagList[j][0]
						nounScores[tagList[j][0]] += 1
	
	nounScores = OrderedDict(sorted(nounScores.items(), key=operator.itemgetter(1)))
	return filterAdj(nounScores, adjDict, phrasesDict)

def filterAdj(nounScores, adjDict, phrasesDict):
	adjectList = list(adjDict.keys())
	finalAdjList = []
	for i in adjectList:
		if (enchVocab.check(str(i)) and len(i) > 2):
			finalAdjList.append(i)

	phrasesDict = OrderedDict(sorted(phrasesDict.items(), key=operator.itemgetter(1), reverse=True))
	newPhrases = dict()

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

	newPhrases = OrderedDict(sorted(newPhrases.items(), key=operator.itemgetter(1), reverse=True))

	"""
	for i, j in newPhrases.items():
		print(i)
	"""

	features = []
	for index, key in enumerate(nounScores):
		value = nounScores[key]
		if value >= 3:
			if "_" in key or (enchVocab.check(str(key)) and len(key) > 2):
				#if "_" in key:
				#	key = key.replace("_", "")
				features.append(key)

	return features, adjectList

"""
nounList = nounScores.keys()
finalAdjList = []
intersect = set(adjectList).intersection(nounList)
adjectList = set(adjectList).difference(intersect)

for i in adjectList:
	if (enchVocab.check(str(i)) and len(i) > 2):
		finalAdjList.append(i)
"""

"""
def intersect(a, b):
    return list(set(a) & set(b))


score = ['canonpowershotg3', 'use', 'picture', 'picturequality', 'camera', 'dial', 'viewfinder', 'speed', 'autosetting', 'canong3', 'photoquality', 'feature', 'darndiopteradjustmentdial', 'exposurecontrol', 'meteringoption', 'spotmetering', '4mp', 'zoom', 'focus', 'size', 'design', 'lcd', 'opticalzoom', 'software', 'lenscap', 'menu', 'control', 'camera', 'print', 'battery', 'photo', 'manualmode', 'feel', 'fourmegapixel', 'product', 'nightmode', 'lenscover', 'zoominglever', 'color', 'price', 'grain', 'flashphoto', 'g3', 'lagtime', 'depth', 'flash', 'externalflashhotshoe', 'image', 'rawimage', 'batterylife', 'manualfunction', 'service', 'automode', 'canon', 'rawformat', 'shape', 'lightautocorrection', 'whiteoffset', 'lowlightfocus', 'unresponsiveness', 'delay', '4mpcamera', 'body', 'casing', 'performance', 'look', 'finish', 'tiffformat', 'lag', 'import', 'manual', 'stitchpicture', 'display', 'compactflash', 'noise', 'automode', 'memorycard', 'made', 'lens', 'lever', 'strap', 'option', 'learning', 'imagequality', 'function', 'macro', '4mpresolution', 'distortion', 'shot', 'remote', 'hotshoeflash', 'batterychargingsystem', 'highlight', 'nooffbutton', 'download', 'optic', 'digitalcamera', 'quality', 'weight']

#score = set(score)

intersection = intersect(nouns,score)
#print "Length of intersection : ",str(len(intersection))
#print "Length of Predicted : ",str(len(nouns))
#print "Length of Actual : ",str(len(score))
print "Precision : ",str(len(intersection)*1.0/len(nouns))
print "Recall : " , str((len(intersection)*1.0)/len(score))
"""
		
	
