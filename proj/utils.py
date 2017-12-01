#Projecto Part2

from math import log
from collections import Counter
import numpy as np
import nltk
import os
from nltk.tokenize import RegexpTokenizer
from sklearn.metrics.pairwise import cosine_similarity

def getString(file):
	text = ''
	with open(file, 'r', encoding = 'ISO-8859-1') as f:
		for line in f:
			text += line
	return text

def getRelevantSummaries():
	path = './test_pt/'
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
	sentNum = 0
	sentList = []
	invIndex = {}
	for doc in documents:
		sentList.append(wordCounter(doc))
	for doc in sentList:
		for word in doc:
			if word not in invIndex:
				invIndex[word] = [[sentNum + 1, doc[word]]]
			else:
				invIndex[word].append([sentNum + 1, doc[word], ])
		sentNum += 1
	return (invIndex, sentNum)

def idfDict(invIndex):
	idfDict = {}
	for word in invIndex[0]:
		idfDict[word] = log(invIndex[1] / len(invIndex[0][word]))
	return idfDict

def tfDict(query):
	tfDict = {}
	tfQuery = wordCounter(query)
	if len(tfQuery) != 0:
		maxTF = max(tfQuery.values())
	for word in tfQuery:
		tfDict[word] = tfQuery[word] / maxTF
	return tfDict

def sparseVector(invIndex, idfDict, query):
	tfD = tfDict(query)
	matrix = np.zeros((1, len(invIndex[0])))
	wordInd = 0
	for word in invIndex[0]:
		if word in tfD:
			tfidf = tfD[word] * idfDict[word]
			matrix[0, wordInd] = tfidf
		wordInd += 1
	return matrix

def sparseMatrix(invIndex, idfDict, documents):
	sparseMatrix = sparseVector(invIndex, idfDict, documents[0])
	for query in documents[1:]:
		nextVector = sparseVector(invIndex, idfDict, query)
		sparseMatrix = np.concatenate((sparseMatrix, nextVector), axis = 0)
	return sparseMatrix

def docSimilarity(corpus, query):
	invIndex = invertedIndex(corpus)
	idfD = idfDict(invIndex)
	documentsMatrix = sparseMatrix(invIndex, idfD, corpus)
	queryVector = sparseVector(invIndex, idfD, query)
	similarity = cosine_similarity(documentsMatrix, queryVector)
	return similarity

def getTopSentences(dictionary, sentencesList, sort = False):
	sentencesID = sorted(dictionary, key = dictionary.get, reverse = True)[:5]
	if sort:
		sentencesID.sort()
	topSentences = []
	for ID in sentencesID:
		topSentences.append(sentencesList[ID])
	return topSentences

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