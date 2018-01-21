
"""
The main code which runs the entire review analysis
"""

import sys
import HAC
import math
import FileCreationWithBigrams
import AdjScore
import operator
import collections
from textblob import TextBlob
from texttable import Texttable

#Get the review filename as command line argument
filename = sys.argv[1]

#reviewTitle is the list containing title of all reviews
reviewTitle = []

#reviewContent is the list containing all reviews
reviewContent = []

posCount = 0
negCount = 0
neutCount = 0
curIndex = -1

#Arrays holding the index of the reviews
posActIndex = []
negActIndex = []
neutActIndex = []

#Extract review title and content from the file
with open(filename) as f:
	review = []
	for line in f:
		if line[:6] == "[+][t]":							#Incase the line starts with [t], then its the title of review
			if review:
				reviewContent.append(review)
				review = []
			reviewTitle.append(line.split("[+][t]")[1].rstrip("\r\n"))
			posCount += 1
			curIndex += 1
			posActIndex.append(curIndex)
		elif line[:6] == "[-][t]":
			if review:
				reviewContent.append(review)
				review = []
			reviewTitle.append(line.split("[-][t]")[1].rstrip("\r\n"))
			negCount += 1
			curIndex += 1
			negActIndex.append(curIndex)
		elif line[:6] == "[N][t]":
			if review:
				reviewContent.append(review)
				review = []
			reviewTitle.append(line.split("[N][t]")[1].rstrip("\r\n"))
			neutCount += 1
			curIndex += 1
			neutActIndex.append(curIndex)
		else:
			if "##" in line:								#Each line in review starts with '##'
				x = line.split("##")
				for i in range(1, len(x)):			#x[0] is the feature given the file.Its been ignored here as its not a part of the review
					review.append(x[i].rstrip("\r\n"))
			else:
				continue
	reviewContent.append(review)

#Creating a File attaching Bigrams
FileCreationWithBigrams.fileCreation(reviewContent,filename)

import MOS
import WithNgrams

#The HAC algorithm to extract features and adjectives in the review
adjDict = HAC.findFeatures(reviewContent,filename)
featureList = WithNgrams.getList()

#Get adjective scores for each adjective
adjScores = AdjScore.getScore(adjDict,filename)

#MOS algorithm to get feature score and review score
posPredIndex, negPredIndex, neutPredIndex, avgFeatScore = MOS.rankFeatures(adjScores, featureList, 
	reviewTitle, reviewContent)

#Write the predicted positive reviews to a file
with open("positiveReviews.txt", "w") as filePos:
	for i in posPredIndex:
		for k in range(len(reviewContent[i])):
			filePos.write(reviewContent[i][k])
		filePos.write("\n")

#Write the predicted negative reviews to a file
with open("negativeReviews.txt", "w") as fileNeg:
	for i in negPredIndex:
		for k in range(len(reviewContent[i])):
			fileNeg.write(reviewContent[i][k])
		fileNeg.write("\n")

#Write the predicted neutral reviews to a file
with open("neutralReviews.txt", "w") as fileNeut:
	for i in neutPredIndex:
		for k in range(len(reviewContent[i])):
			fileNeut.write(reviewContent[i][k])
		fileNeut.write("\n")

#Write the predicted neutral reviews to a file
with open("featureScore.txt", "w") as fileFeat:
	t = Texttable()
	lst = [["Feature", "Score"]]
	for tup in avgFeatScore:
		lst.append([tup[0], tup[1]])
	t.add_rows(lst)
	fileFeat.write(str(t.draw()))

print("The files are successfully created.")

#Evaluation metric
PP = len(set(posActIndex).intersection(set(posPredIndex)))
PNe = len(set(posActIndex).intersection(set(negPredIndex)))
PN = len(set(posActIndex).intersection(set(neutPredIndex)))

NeP = len(set(negActIndex).intersection(set(posPredIndex)))
NeNe = len(set(negActIndex).intersection(set(negPredIndex)))
NeN = len(set(negActIndex).intersection(set(neutPredIndex)))

NP = len(set(neutActIndex).intersection(set(posPredIndex)))
NNe = len(set(neutActIndex).intersection(set(negPredIndex)))
NN = len(set(neutActIndex).intersection(set(neutPredIndex)))

#Draw the confusion matrix table
t = Texttable()
t.add_rows([['', 'Pred +', 'Pred -', 'Pred N'], ['Act +', PP, PNe, PN], ['Act -', NeP, NeNe, NeN], ['Act N', NP, NNe, NN]])
print("Evaluation metric - Confusion matrix:")
print("=====================================")
print("Dataset:", filename)
print(t.draw())