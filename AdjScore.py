"""
   This code neglects the meaningless adjectives, and gives score to the remaining ones in the range [-4. 4]
"""
from textblob import TextBlob
import operator
from collections import OrderedDict

"""
Each adjective is given a score (depending on its polarity).
These scores then determine the avg score of each feature.
"""

#Return the adjective scores for adjectives in adjList
def getScore(adjList):

	inversion_words = []
	adjScores = dict()

	for i in adjList:
		blob = TextBlob(i)
		if(blob.sentiment.polarity != 0):
			#If the adjective expresses some polarity
			adjScores[i] = blob.sentiment.polarity

	#Multiply the polarity by 4 to get in the given range
	adjScores.update((x, 4 * y) for x, y in adjScores.items())
	adjScores = sorted(adjScores.items(), key=operator.itemgetter(1), reverse=True)

	#Print the adjectives and their scores
	return(OrderedDict(adjScores))