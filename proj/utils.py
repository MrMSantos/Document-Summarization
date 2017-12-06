#Projecto Part2

from math import log
from collections import Counter
import numpy as np
import pickle
import nltk
import os
from nltk.tokenize import RegexpTokenizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import normalize

def getString(file):
	text = ''
	with open(file, 'r', encoding = 'ISO-8859-1') as f:
		for line in f:
			text += line
	return text

def getRelevantSummaries():
	path = './corpus_test/test_set/'
	summaries = []
	for doc in os.listdir(path):
		summary = getString(path + doc)
		summary = getSentences(summary)
		summaries.append(summary)
	return summaries

def getSentences(string, language = 'portuguese'):
    sentences = []
    stringSplit = string.split('\n\n')
    for string in stringSplit:
        sent = nltk.sent_tokenize(string, language)
        sentences += sent
    return sentences

def ngrams(document, n):
	words = nltk.word_tokenize(document)
	ngram = nltk.ngrams(words, n)
	ngramCounter = Counter(ngram)
	return ngramCounter

def wordCounter(document):
	tokenizer = RegexpTokenizer(r'\w+')
	sent = tokenizer.tokenize(document)
	sent = ' '.join(sent)
	sent = sent.lower()
	counter = ngrams(sent, 1)
	return counter

def invertedIndex(documents):
	sentList = []
	invIndex = {}
	for doc in documents:
		sentList.append(wordCounter(doc))
	for doc in sentList:
		for word in doc:
			if word[0] not in invIndex:
				invIndex[word[0]] = 1
			else:
				invIndex[word[0]] += 1
	for word in invIndex:
		wordIDF = log(len(documents) / invIndex[word])
		invIndex[word] = (invIndex[word], wordIDF)
	return invIndex

def tfDict(query):
	tfDict = {}
	tfQuery = wordCounter(query)
	if len(tfQuery) != 0:
		maxTF = max(tfQuery.values())
	for word in tfQuery:
		tfDict[word[0]] = tfQuery[word] / maxTF
	return tfDict

def sparseVector(invIndex, query):
	tfD = tfDict(query)
	matrix = np.zeros((1, len(invIndex)))
	wordInd = 0
	for word in invIndex:
		if word in tfD:
			tfidf = tfD[word] * invIndex[word][1]
			matrix[0, wordInd] = tfidf
		wordInd += 1
	return matrix

def sparseMatrix(invIndex, documents):
	sparseMatrix = sparseVector(invIndex, documents[0])
	for query in documents[1:]:
		nextVector = sparseVector(invIndex, query)
		sparseMatrix = np.concatenate((sparseMatrix, nextVector), axis = 0)
	return sparseMatrix

def docSimilarity(invIndex, query1, query2):
	documentsMatrix = sparseMatrix(invIndex, query1)
	queryVector = sparseMatrix(invIndex, query2)
	similarity = cosine_similarity(documentsMatrix, queryVector)
	return similarity

#Trained with nltk.floresta, tagged with unigrams and bigrams
def npSearch(document):
	tagger2 = pickle.load(open('trainer', 'rb'))
	resultTags = tagger2.tag(document.split())
	twords = [(w.lower(), simplify_tag(t)) for (w, t) in resultTags]
	newtwords = []
	for (w, t) in twords:
		newtwords.append((''.join(c for c in w if c not in ('!','.',':', ',')), t))
	grammar = 'NP: {<art>?<n>+<adj>*}'
	cp = nltk.RegexpParser(grammar)
	tree = cp.parse(newtwords)
	nounSent = []
	for subtree in tree.subtrees():
		if subtree.label() == 'NP':
			leaves = subtree.leaves()
			word = ''
			for wordPair in leaves:
				word += wordPair[0] + ' '
			word = word[:-1]
			nounSent.append(word)
	return nounSent

def simplify_tag(t):
	if '+' in t:
		return t[t.index("+") + 1:]
	else:
		return t

def getTopSentences(dictionary, sentencesList, sort = False):
	sentencesID = sorted(dictionary, key = dictionary.get, reverse = True)[:5]
	if sort:
		sentencesID.sort()
	topSentences = []
	for ID in sentencesID:
		topSentences.append(sentencesList[ID])
	return topSentences

def normalizeDict(graph):
	vector = []
	newGraph = {}
	for node in graph:
		vector.append(graph[node])
	normVector = [float(i) / sum(vector) for i in vector]
	i = 0
	for node in graph:
		newGraph[node] = normVector[i]
		i += 1
	return newGraph

def getPrecision(prediction, goal):
	truePositives = 0
	for sentence in prediction:
		if sentence in goal:
			truePositives += 1
	precision = truePositives / len(prediction)
	return precision

def avgPrecision(predList, goalList):
	precisionSum = 0
	for i in range(0, len(predList)):
		if predList[i] in goalList:
			precision = getPrecision(list(predList[:i + 1]), goalList)
			precisionSum += precision
	return precisionSum / len(goalList)

def map(predList, goalList):
	aprecisionSum = 0
	for i in range(0, len(predList)):
		aprecision = avgPrecision(predList[i], goalList[i])
		aprecisionSum += aprecision
	return aprecisionSum / len(predList)