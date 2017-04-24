import nltk
from nltk.corpus import stopwords				#Stopwords module
import string
import operator
from collections import OrderedDict

#Set of all stop words in english
stopWords = stopwords.words("english")

#Remove punctuation from each line in reviews
exclude = set(string.punctuation)

#reviewTitle is the list containing title of all reviews
reviewTitle = []

#reviewContent is the list containing all reviews
#reviewTitle[0] and reviewContent[0] will point to the title and review content of the 1st review
reviewContent = []

#Extract data from the file
with open("Nokia 6610.txt") as f:
	review = []
	for line in f:
		if line[:3] == "[t]":							#Incase the line starts with [t], then its the title of review
			if review:
				reviewContent.append(review)
				review = []
			reviewTitle.append(line.split("[t]")[1].rstrip("\r\n"))
		else:	
			if "##" in line:								#Each line in review starts with '##'
				x = line.split("##")
				for i in xrange(1, len(x)):			#x[0] is the feature given the file.Its been ignored here as its not a part of the review
					review.append(x[i].rstrip("\r\n"))
			else:
				continue
	reviewContent.append(review)

#nounScores is the dict containing nouns from all reviews and their respective scores from HAC algorithm
nounScores = dict()

#adjDict dict contains adjective and the corresponding noun which it is assigned to
adjDict = dict()

#Iterate for all reviews
for a in xrange(len(reviewContent)):
	#Iterate for all lines in the review
	for i in xrange(len(reviewContent[a])):
		#Remove all the stopwords from the line
		text = ' '.join([word for word in reviewContent[a][i].split() if word not in stopwords.words("english")])
	
		#Remove all the punctuation from the line
		text = ''.join(ch for ch in text if ch not in exclude)
		
		#Tokenize the line to assign pos to each word
		text = nltk.word_tokenize(text)
		
		#Assign pos to each word
		x = nltk.pos_tag(text)

		#tagList contains all nouns and adjectives in the line
		tagList = []
		for e in x:
			if(e[1] == "NN" or e[1] == "JJ"):
				tagList.append(e)
	
		#Add the nouns(which are not in the nounScores dict) to the dict
		for e in tagList:
			if e[1] == "NN":
				if e[0] not in nounScores:
					nounScores[e[0]] = 0

		#For every adjective, find nearby noun
		for l in xrange(len(tagList)):
			if(tagList[l][1] == "JJ"):
				j = k = leftHop = rightHop = -1
				
				#Find the closest noun to the right of the adjective in the line
				for j in xrange(l + 1, len(tagList)):
					if(tagList[j][1] == "NN"):
						rightHop = (j - l)
						break

				#Find the closest noun to the left of the adjective in the line
				for k in xrange(l - 1, -1, -1):
					if(tagList[k][1] == "NN"):
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
					
#sort nouns according to their scores
nounScores = OrderedDict(sorted(nounScores.items(), key=operator.itemgetter(1)))

#The loop below shows the nouns that each adjective is assigned to
for key, value in adjDict.iteritems():
	print "Adj:", key, "--> Assigned_Noun:", value

#Uncomment the loop below to show the nouns and their scores in sorted order
#for key, value in nounScores.iteritems():
#	print "Noun:", key, "--> Score:", value

		
		
