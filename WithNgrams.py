

#Finding Noun Scores after Combining N grams

import nltk
from nltk.corpus import stopwords
import string
import operator
from collections import OrderedDict 
#from textblob import TextBlob
from textblob import Blobber
from textblob.taggers import PatternTagger, NLTKTagger
from textblob_aptagger import PerceptronTagger

stopWords = stopwords.words("english")
exclude = set(string.punctuation)
reviewTitle = []
reviewContent = []
def final():
	#reading from the created file "modified.txt"
	with open("modified.txt") as f:
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
					for i in xrange(1, len(x)):
						review.append(x[i].rstrip("\r\n"))
				else:
					continue
		reviewContent.append(review)

	#tb = Blobber(pos_tagger=PerceptronTagger()) 
	tb = Blobber(pos_tagger=NLTKTagger())
	nounScores = dict()
	for a in xrange(len(reviewContent)):								#Stores the score of the nouns
		for i in xrange(len(reviewContent[a])):
			#text = reviewContent[a][i]
			text = ' '.join([word for word in reviewContent[a][i].split() if word not in stopwords.words("english")])
			text = ''.join(ch for ch in text if ch not in exclude)
			text = nltk.word_tokenize(text)
			x = nltk.pos_tag(text)
			#x = TextBlob(text).tags #textblob tagger
			#x = tb(text).tags #Perceptron tagger 
			#Get the noun/adjective words and store it in tagList
			tagList = []
			for e in x:
				if(e[1] == "NN" or e[1] == "JJ"):
					tagList.append(e)
				
			#print tagList
	
			#Add the nouns(which are not in the nounScores dict) to the dict
			for e in tagList:
				if e[1] == "NN":
					if e[0] not in nounScores:
						nounScores[e[0]] = 0

			#For every adjective, find nearby noun
			l=0
			for l in xrange(len(tagList)):
				if(tagList[l][1] == "JJ"):
					check=0
					j=0
					k=0
					ct1=0
					for j in xrange(l + 1, len(tagList)):
						if ct1 == 4:
							break
						if(tagList[j][1] == "NN"):
							#nounScores[tagList[j][0]] += 1
							check=1
							break
					ct=0		
					if(l>0):
						if j==0:
							j = len(tagList)
						for k in xrange(l-1,0,-1):
							if ct == 4:
								break
							ct=ct+1
							if(tagList[k][1] == "NN"):
								if(j != len(tagList)):
									nounScores[tagList[min(j,k)][0]] += 1
								else:
									nounScores[tagList[k][0]] += 1	
								break
					elif check==1:
						nounScores[tagList[j][0]] += 1
	
	nounScores = OrderedDict(sorted(nounScores.items(), key=operator.itemgetter(1)))
	nouns = []
	for key, value in nounScores.items():
		#print("Noun:", key, "--> Score:", value)
		if value >= 3:
			nouns.append(key)
			print key," : ",value
	return nouns
	#nouns = set(nouns)

def intersect(a, b):
    return list(set(a) & set(b))

"""
score = ['canonpowershotg3', 'use', 'picture', 'picturequality', 'camera', 'dial', 'viewfinder', 'speed', 'autosetting', 'canong3', 'photoquality', 'feature', 'darndiopteradjustmentdial', 'exposurecontrol', 'meteringoption', 'spotmetering', '4mp', 'zoom', 'focus', 'size', 'design', 'lcd', 'opticalzoom', 'software', 'lenscap', 'menu', 'control', 'camera', 'print', 'battery', 'photo', 'manualmode', 'feel', 'fourmegapixel', 'product', 'nightmode', 'lenscover', 'zoominglever', 'color', 'price', 'grain', 'flashphoto', 'g3', 'lagtime', 'depth', 'flash', 'externalflashhotshoe', 'image', 'rawimage', 'batterylife', 'manualfunction', 'service', 'automode', 'canon', 'rawformat', 'shape', 'lightautocorrection', 'whiteoffset', 'lowlightfocus', 'unresponsiveness', 'delay', '4mpcamera', 'body', 'casing', 'performance', 'look', 'finish', 'tiffformat', 'lag', 'import', 'manual', 'stitchpicture', 'display', 'compactflash', 'noise', 'automode', 'memorycard', 'made', 'lens', 'lever', 'strap', 'option', 'learning', 'imagequality', 'function', 'macro', '4mpresolution', 'distortion', 'shot', 'remote', 'hotshoeflash', 'batterychargingsystem', 'highlight', 'nooffbutton', 'download', 'optic', 'digitalcamera', 'quality', 'weight']

#score = set(score)

intersection = intersect(nouns,score)
#print "Length of intersection : ",str(len(intersection))
#print "Length of Predicted : ",str(len(nouns))
#print "Length of Actual : ",str(len(score))
print "Precision : ",str(len(intersection)*1.0/len(nouns))
print "Recall : " , str((len(intersection)*1.0)/len(score))
"""
		
	
