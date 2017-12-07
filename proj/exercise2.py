#Projecto Part2

from utils import getString, getSentences, getTopSentences
from utils import getRelevantSummaries, map
from utils import invertedIndex, docSimilarity, npSearch
from exercise1 import createGraph, docSummaryEx1
from nltk.tokenize import RegexpTokenizer
import nltk
import os

#Prior Functions
def nodePriorSimilarity(invIndex, sentenceList, document):
	priorDict = {}
	sentSimilarity = docSimilarity(invIndex, sentenceList, [document])
	for sentenceID in range(0, len(sentSimilarity)):
		priorDict[sentenceID] = sentSimilarity[sentenceID][0]
	return priorDict

def nodePriorScores(invIndex, sentenceList, document):
	priorDict = {}
	for sentenceID in range(0, len(sentenceList)):
		score = 0
		words = nltk.word_tokenize(sentenceList[sentenceID], language = 'portuguese')
		for word in words:
			if word in invIndex:
				score += invIndex[word][0]
		priorDict[sentenceID] = score
	return priorDict

def nodePriorPosition(sentenceList, document):
	priorDict = {}
	tokenizer = RegexpTokenizer(r'\w+')
	for sentenceID in range(0, len(sentenceList)):
		sent = tokenizer.tokenize(sentenceList[sentenceID])
		priorDict[sentenceID] =  len(sent) / (sentenceID + 1)
	return priorDict

def nodePriorDegree(graph, sentenceList):
	priorDict = {}
	for node in range(0, len(sentenceList)):
		if node in graph:
			priorDict[node] = len(graph[node])
		else:
			priorDict[node] = 0
	return priorDict

def nodePriorNoun(sentenceList):
	priorDict = {}
	for i in range(0, len(sentenceList)):
		nodeNouns = npSearch(sentenceList[i])
		priorDict[i] = len(nodeNouns)
	return priorDict

#Weight Functions
def edgeWeightSimilarity(invIndex, graph, sentenceList):
	weightDict = {}
	for node in graph:
		for edge in graph[node]:
			if (node, edge) not in weightDict and (edge, node) not in weightDict:
				sentSimilarity = docSimilarity(invIndex, [sentenceList[node]], [sentenceList[edge]])
				weightDict[(node, edge)] = sentSimilarity[0][0]
				weightDict[(edge, node)] = sentSimilarity[0][0]
	return weightDict

def edgeWeightNoun(graph, sentenceList):
	weightDict = {}
	for node in graph:
		for edge in graph[node]:
			if (node, edge) not in weightDict and (edge, node) not in weightDict:
				nounCount = 0
				nodeNouns = npSearch(sentenceList[node])
				linkedNodeNouns = npSearch(sentenceList[edge])
				for noun in nodeNouns:
					if noun in linkedNodeNouns:
						nounCount += 1
				weightDict[(node, edge)] = nounCount
				weightDict[(edge, node)] = nounCount
	return weightDict

def edgeWeightScores(graph, invIndex, sentenceList, document):
	weightDict = {}

	for node in graph:
		nodeWords = nltk.word_tokenize(sentenceList[node], language = 'portuguese')
		for edge in graph[node]:
			if (node, edge) not in weightDict and (edge, node) not in weightDict:
				commonWordsCount = 0
				linkedNodeWords = nltk.word_tokenize(sentenceList[edge], language = 'portuguese')
				for word in nodeWords:
					if word in linkedNodeWords:
						commonWordsCount += 1
				weightDict[(node, edge)] = commonWordsCount / len(invIndex)
				weightDict[(edge, node)] = commonWordsCount / len(invIndex)
	return weightDict

def pageRankOpt(graph, priorDict, weightDict, df = 0.15, maxIterations = 50):
	pRankDict = {}
	graphLen = len(graph)
	uniformProbability = 1 / graphLen
	for node in graph:
		pRankDict[node] = uniformProbability
	for _ in range(0, maxIterations):
		auxDict = {}
		for node in graph:
			discountFactor = df * priorDict[node]
			priorSum = 0
			linkSum = 0
			for linkedNode in graph[node]:
				priorSum += priorDict[linkedNode]
				linkSumNum = pRankDict[linkedNode] * weightDict[(node, linkedNode)]
				edgeSum = 0
				for edgeNode in graph[linkedNode]:
					edgeSum += weightDict[(linkedNode, edgeNode)]
				if edgeSum == 0:
					linkSum = 0
				else:
					linkSum += linkSumNum / edgeSum
			if priorSum == 0:
				auxDict[node] = 0
			else:
				auxDict[node] = (discountFactor / priorSum) + ((1 - df) * linkSum)
		pRankDict = auxDict
	return pRankDict

def docSummaryEx2(document):
	if isinstance(document, str):
		documentString = getString(document)
		document = getSentences(documentString)
	invIndex = invertedIndex(document)
	graphDict = createGraph(document, invIndex)

	#Prior Functions
	priorDict = nodePriorPosition(document, documentString)
	#priorDict = nodePriorSimilarity(invIndex, document, documentString)
	#priorDict = nodePriorDegree(graphDict, document)
	#priorDict = nodePriorScores(invIndex, document, documentString)
	#priorDict = nodePriorNoun(document)

	#Weight Functions
	weightDict = edgeWeightScores(graphDict, invIndex, document, documentString)
	#weightDict = edgeWeightSimilarity(invIndex, graphDict, document)
	#weightDict = edgeWeightNoun(graphDict, document)

	pRankDict = pageRankOpt(graphDict, priorDict, weightDict)
	topSentences = getTopSentences(pRankDict, document)
	return topSentences

#Summaries for exercise 1
def getPredictedSummariesEx1():
	path = './corpus_test/train_set/'
	summaries = []
	for doc in os.listdir(path):
		summary = docSummaryEx1(path + doc)
		summaries.append(summary)
	return summaries

#Summaries for exercise 2
def getPredictedSummariesEx2():
	path = './corpus_test/train_set/'
	summaries = []
	for doc in os.listdir(path):
		summary = docSummaryEx2(path + doc)
		summaries.append(summary)
	return summaries


def main():
	print("Calculating MAP for exercise 1")
	predictedSum = getPredictedSummariesEx1()
	relevantSum = getRelevantSummaries()
	MAP = map(predictedSum, relevantSum)
	print('Mean Average Precision:', MAP)

	print("Calculating MAP for exercise 2")
	predictedSum = getPredictedSummariesEx2()
	relevantSum = getRelevantSummaries()
	MAP = map(predictedSum, relevantSum)
	print('Mean Average Precision:', MAP)

if __name__ == '__main__':
	main()
