import sys
import HAC

#Get the filename as command line argument
filename = sys.argv[1]

#reviewTitle is the list containing title of all reviews
reviewTitle = []

#reviewContent is the list containing all reviews
#reviewTitle[0] and reviewContent[0] will point to the title and review content of the 1st review
reviewContent = []

#Extract data from the file
with open(filename) as f:
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
				for i in range(1, len(x)):			#x[0] is the feature given the file.Its been ignored here as its not a part of the review
					review.append(x[i].rstrip("\r\n"))
			else:
				continue
	reviewContent.append(review)

nounScores, adjDict = HAC.findFeatures(reviewContent)