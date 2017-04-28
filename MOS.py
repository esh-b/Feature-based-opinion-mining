import re
import string
import operator
import collections
from textblob import TextBlob
from nltk.corpus import stopwords

adj_scores = collections.OrderedDict([('awesome', 4.0), ('excellent', 4.0), ('wonderful', 4.0), ('ideal', 3.6), ('incredible', 3.6), \
			 ('beautiful', 3.4), ('great', 3.2), ('happy', 3.2), ('bright', 2.8000000000000003), ('nice', 2.4), \
			 ('love', 2.0), ('creative', 2.0), ('able', 2.0), ('satisfied', 2.0), ('pleased', 2.0), ('sophisticated', 2.0), \
			 ('easy', 1.7333333333333334), ('fantastic', 1.6), ('advanced', 1.6), ('fabulous', 1.6), ('light', 1.6), \
			 ('comfortable', 1.6), ('available', 1.6), ('clean', 1.4666666666666668), ('quick', 1.3333333333333333), \
			 ('super', 1.3333333333333333), ('worth', 1.2), ('powerful', 1.2), ('first', 1.0), ('positive', 0.9090909090909091), \
			 ('ready', 0.8), ('real', 0.8), ('reasonable', 0.8), ('fast', 0.8), ('much', 0.8), ('main', 0.6666666666666666), \
			 ('high', 0.64), ('live', 0.5454545454545454), ('clear', 0.4000000000000001), ('flat', -0.1), ('minor', -0.2), \
			 ('single', -0.2857142857142857), ('remote', -0.4), ('partially', -0.4), ('extreme', -0.5), ('sharp', -0.5), \
			 ('average', -0.6), ('heavy', -0.8), ('harsh', -0.8), ('raw', -0.9230769230769231), ('small', -1.0), \
			 ('hard', -1.1666666666666667), ('slow', -1.2000000000000002), ('serious', -1.3333333333333333), \
			 ('disappointing', -2.4), ('bad', -2.7999999999999994)])

#adj_scores = collections.OrderedDict([('incredible', 3.6), ('brilliant', 3.6), ('ideal', 3.6), ('happy', 3.2), ('great', 3.2), ('remarkable', 3.0), ('good', 2.8), ('superior', 2.8), ('exceptional', 2.6666666666666665), ('amazing', 2.4000000000000004), ('nicely', 2.4), ('spectacular', 2.4), ('creative', 2.0), ('top', 2.0), ('able', 2.0), ('reputable', 2.0), ('satisfied', 2.0), ('pleased', 2.0), ('sophisticated', 2.0), ('precious', 2.0), ('outstanding', 2.0), ('many', 2.0), ('huge', 1.6000000000000003), ('available', 1.6), ('fantastic', 1.6), ('fit', 1.6), ('comfortable', 1.6), ('important', 1.6), ('cheap', 1.6), ('fabulous', 1.6), ('advanced', 1.6), ('unique', 1.5), ('friendly', 1.5), ('clean', 1.4666666666666668), ('true', 1.4), ('full', 1.4), ('quick', 1.3333333333333333), ('artistic', 1.3333333333333333), ('tremendous', 1.3333333333333333), ('super', 1.3333333333333333), ('powerful', 1.2), ('useful', 1.2), ('hot', 1.0), ('first', 1.0), ('positive', 0.9090909090909091), ('certain', 0.8571428571428571), ('large', 0.8571428571428571), ('absolute', 0.8), ('reasonable', 0.8), ('modern', 0.8), ('much', 0.8), ('ready', 0.8), ('whole', 0.8), ('real', 0.8), ('realistic', 0.6666666666666666), ('main', 0.6666666666666666), ('steady', 0.6666666666666666), ('high', 0.64), ('live', 0.5454545454545454), ('new', 0.5454545454545454), ('clear', 0.4000000000000001), ('direct', 0.4), ('professional', 0.4), ('seamless', 0.4), ('natural', 0.4), ('complete', 0.4), ('major', 0.25), ('general', 0.20000000000000007), ('flat', -0.1), ('minor', -0.2), ('long', -0.2), ('limited', -0.2857142857142857), ('single', -0.2857142857142857), ('loose', -0.3076923076923077), ('wide', -0.4), ('minimal', -0.4), ('due', -0.5), ('extreme', -0.5), ('sharp', -0.5), ('average', -0.6), ('previous', -0.6666666666666666), ('subject', -0.6666666666666666), ('little', -0.75), ('wasted', -0.8), ('green', -0.8), ('heavy', -0.8), ('harsh', -0.8), ('raw', -0.9230769230769231), ('small', -1.0), ('usual', -1.0), ('hard', -1.1666666666666667), ('negative', -1.2), ('shaky', -1.3333333333333333), ('serious', -1.3333333333333333), ('tough', -1.5555555555555556), ('poor', -1.6), ('difficult', -2.0), ('expensive', -2.0), ('needless', -2.0), ('casual', -2.0000000000000004), ('awkward', -2.4), ('bad', -2.7999999999999994), ('disappointed', -3.0), ('idiot', -3.2), ('rank', -3.2), ('terrible', -4.0), ('horrible', -4.0)])
features = ["bit","focus","metering","cameracanon","computer","price","power","unit","strap","range","alsmost","snug","picturequality","postagestamp",\
	"fire","detail","spin","bargain","balance","canon","film","builtin","picture","curve","m","anybody","criticsm","reputation","position","menus","read",\
	"auto","lcd","point","magnesium","anyone","lot","whitecorrection","life","something","functionality","design","adjustment","flash","thing","priority",\
	"system","viewfinder","g3","control","time","mode","battery","software","quality","zoom","use","camera"]

apostropheList = {"n't" : "not","aren't" : "are not","can't" : "cannot","couldn't" : "could not","didn't" : "did not","doesn't" : "does not","don't" : "do not","hadn't" : "had not","hasn't" : "has not","haven't" : "have not","he'd" : "he had","he'll" : "he will","he's" : "he is","I'd" : "I had","I'll" : "I will","I'm" : "I am","I've" : "I have","isn't" : "is not","it's" : "it is","let's" : "let us","mustn't" : "must not","shan't" : "shall not","she'd" : "she had","she'll" : "she will","she's" : "she is","shouldn't" : "should not","that's" : "that is","there's" : "there is","they'd" : "they had","they'll" : "they will","they're" : "they are","they've" : "they have","we'd" : "we had","we're" : "we are","we've" : "we have","weren't" : "were not","what'll" : "what will","what're" : "what are","what's" : "what is","what've" : "what have","where's" : "where is","who'd" : "who had","who'll" : "who will","who're" : "who are","who's" : "who is","who've" : "who have","won't" : "will not","wouldn't" : "would not","you'd" : "you had","you'll" : "you will","you're" : "you are","you've" : "you have"}

stopWords = stopwords.words("english")
exclude = set(string.punctuation)
reviewTitle = []
reviewContent = []
alpha = 0.2

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

reviewOTitle = []
reviewOContent = []
with open("Canon G3.txt") as f:
	review = []
	for line in f:
		if line[:3] == "[t]":
			if review:
				reviewOContent.append(review)
				review = []
			reviewOTitle.append(line.split("[t]")[1].rstrip("\r\n"))
		else:	
			if "##" in line:
				x = line.split("##")
				for i in range(1, len(x)):
					review.append(x[i].rstrip("\r\n"))
			else:
				continue
	reviewOContent.append(review)

def rankFeatures(adj_scores, features):

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

pos_review_list, neg_review_list, avg_score = rankFeatures(adj_scores, features)
pos_review_list = collections.OrderedDict(sorted(pos_review_list.items(), key=operator.itemgetter(1), reverse=True))
neg_review_list = collections.OrderedDict(sorted(neg_review_list.items(), key=operator.itemgetter(1)))


for i in range(10):
	print("###", reviewOTitle[i])
	print(''.join(reviewOContent[i]))

