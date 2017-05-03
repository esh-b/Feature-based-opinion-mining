"""
  The MOS algorithm implementation - Classification of reviews and calculation of feature scores
"""

import re
import string
import operator
from collections import OrderedDict
from textblob import TextBlob
from nltk.corpus import stopwords
import os


#Dict to convert the raw user text to meaningful words for analysis
apostropheList = {"n't" : "not","aren't" : "are not","can't" : "cannot","couldn't" : "could not","didn't" : "did not","doesn't" : "does not", \
				  "don't" : "do not","hadn't" : "had not","hasn't" : "has not","haven't" : "have not","he'd" : "he had","he'll" : "he will", \
				  "he's" : "he is","I'd" : "I had","I'll" : "I will","I'm" : "I am","I've" : "I have","isn't" : "is not","it's" : \
				  "it is","let's" : "let us","mustn't" : "must not","shan't" : "shall not","she'd" : "she had","she'll" : "she will", \
				  "she's" : "she is", "shouldn't" : "should not","that's" : "that is","there's" : "there is","they'd" : "they had", \
				  "they'll" : "they will", "they're" : "they are","they've" : "they have","we'd" : "we had","we're" : "we are","we've" : "we have", \
				  "weren't" : "were not", "what'll" : "what will","what're" : "what are","what's" : "what is","what've" : "what have", \
				  "where's" : "where is","who'd" : "who had", "who'll" : "who will","who're" : "who are","who's" : "who is","who've" : "who have", \
				  "won't" : "will not","wouldn't" : "would not", "you'd" : "you had","you'll" : "you will","you're" : "you are","you've" : "you have"}

#Removing stop words might lead to better data analysis
stopWords = stopwords.words("english")

#Exclude punctuations from the reviews
exclude = set(string.punctuation)

#The two lists which holds the review title and the corresponding reviews
reviewTitle = []
reviewContent = []
alpha = 0.6

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
				for i in range(1, len(x)):
					review.append(x[i].rstrip("\r\n"))
			else:
				continue
	reviewContent.append(review)

def rankFeatures(adj_scores, features, reviewTitle, reviewContent):

	#Lists containing indices of the reviewContent list
	pos_review_index = dict()
	neg_review_index = dict()

	#scores for a feature from all the reviews
	global_noun_scores = dict()

	#Number of adj describing a feature obtained from all the reviews
	global_noun_adj_count = dict()

	#Iterate for each review in the list of reviews
	for a in range(len(reviewContent)):

		#scores for a feature from the review
		review_noun_scores = dict()
		title_noun_scores = dict()

		#Number of adj describing a feature in the review
		review_noun_adj_count = dict()
		title_noun_adj_count = dict()

		#Iterate for all lines in a review
		for lineIndex in range(len(reviewContent[a]) + 1):
			if(lineIndex == len(reviewContent[a])):
				line_words = reviewTitle[a]
			else:
				line_words = reviewContent[a][lineIndex]

			line_words = ' '.join([apostropheList[word] if word in apostropheList else word for word in line_words.split()])
			line_words = ''.join(ch for ch in line_words if ch not in exclude)
			line_words = re.sub(r' [a-z][$]? ', ' ', line_words)
			line_words = [word for word in line_words.split() if(word not in stopwords.words("english") and not word.isdigit()) and len(word) > 2]

			#Iterate for each word in the line
			for wordIndex in range(len(line_words)):
				word = line_words[wordIndex]

				#If the word is an adj, get the adj score and check for inversion words onto its left
				if word in adj_scores:
					score = adj_scores[word]

					#Left context for inversion words
					if(wordIndex - 2 >= 0):

						#Phrase is the last two words and the present adj
						phrase = line_words[wordIndex - 2] + " " + line_words[wordIndex - 1] + " " + line_words[wordIndex]

						#If the polarity of the phrase and the adj is opposite
						if((TextBlob(phrase).sentiment.polarity * score) < 0):
							score *= -1
					elif(wordIndex - 1 >= 0):

						#Phrase is the last word and the present adj
						phrase = line_words[wordIndex - 1] + " " + line_words[wordIndex]

						#If the polarity of the phrase and the adj is opposite
						if((TextBlob(phrase).sentiment.polarity * score) < 0):
							score *= -1

					#Find the closest feature to the adj
					closest_noun = find_closest_noun(wordIndex, line_words, features)
					if(closest_noun is None):
						continue

					if(lineIndex == len(reviewContent[a])):
						if(closest_noun in title_noun_scores):
							title_noun_scores[closest_noun] += score
						else:
							title_noun_scores[closest_noun] = score

						#Increase the count of no of adjs describing the feature
						if(closest_noun in title_noun_adj_count):
							title_noun_adj_count[closest_noun] += 1
						else:
							title_noun_adj_count[closest_noun] = 1

					else:
						#Update the score of the feature which the adj is describing
						if(closest_noun in review_noun_scores):
							review_noun_scores[closest_noun] += score
						else:
							review_noun_scores[closest_noun] = score

						if(closest_noun in global_noun_scores):
							global_noun_scores[closest_noun] += score
						else:
							global_noun_scores[closest_noun] = score

						#Increase the count of no of adjs describing the feature
						if(closest_noun in review_noun_adj_count):
							review_noun_adj_count[closest_noun] += 1
						else:
							review_noun_adj_count[closest_noun] = 1

						if(closest_noun in global_noun_adj_count):					
							global_noun_adj_count[closest_noun] += 1
						else:
							global_noun_adj_count[closest_noun] = 1

		#Score for the review content
		total_score = sum(review_noun_scores.values())
		total_adj = sum(review_noun_adj_count.values())

		if(total_adj == 0):
			review_score = 0
		else:
			review_score = total_score / float(total_adj)

		#Find the title score
		title_total_score = sum(title_noun_scores.values())
		title_total_adj = sum(title_noun_adj_count.values())

		if(title_total_adj == 0):
			title_score = 0
		else:
			title_score = title_total_score / float(title_total_adj)

		#The total score for the review
		avg_score = ((alpha * title_score) + review_score) / (alpha + 1)

		#Incase both title_score and review_scores are 0's, then ignore that review
		if(avg_score == 0):
			continue

		if(avg_score > 0):
			pos_review_index[a] = avg_score
		else:
			neg_review_index[a] = avg_score

	#Scores for each feature from all the reviews
	avg_feature_score = dict()
	for noun in global_noun_scores:
		avg_feature_score[noun] = global_noun_scores[noun] / float(global_noun_adj_count[noun])
	avg_feature_score = sorted(avg_feature_score.items(), key=operator.itemgetter(1), reverse=True)

	pos_review_index = OrderedDict(sorted(pos_review_index.items(), key=operator.itemgetter(1), reverse=True))
	neg_review_index = OrderedDict(sorted(neg_review_index.items(), key=operator.itemgetter(1)))

	#os.remove("modified.txt")
	return pos_review_index, neg_review_index, avg_feature_score

#Find the closest feature for an adj. Assumes a noun is found within 3 steps from the adj.
def find_closest_noun(wordIndex, line_words, features):
	ptr = 1
	while(ptr <= 3):
		if(wordIndex + ptr < len(line_words) and line_words[wordIndex + ptr] in features):
			return line_words[wordIndex + ptr]
		elif(wordIndex - ptr >= 0 and line_words[wordIndex - ptr] in features):
			return line_words[wordIndex - ptr]
		else:
			ptr += 1

