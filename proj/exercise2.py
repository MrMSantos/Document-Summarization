#Projecto Part2

from utils import getString, getSentences, getTopSentences
from utils import getRelevantSummaries, map
from utils import invertedIndex, docSimilarity
from exercise1 import createGraph, docSummaryEx1
import os

def nodePriorSimilarity(invIndex, sentenceList, document):
	priorDict = {}
	sentSimilarity = docSimilarity(invIndex, sentenceList, [document])
	for sentenceID in range(0, len(sentSimilarity)):
		priorDict[sentenceID] = sentSimilarity[sentenceID][0]
	return priorDict

def edgeWeightSimilarity(invIndex, graph, sentenceList):
	weightDict = {}
	for node in graph:
		for edge in graph[node]:
			if (node, edge) not in weightDict and (edge, node) not in weightDict:
				sentSimilarity = docSimilarity(invIndex, [sentenceList[node]], [sentenceList[edge]])
				weightDict[(node, edge)] = sentSimilarity[0][0]
				weightDict[(edge, node)] = sentSimilarity[0][0]
	return weightDict

def pageRankOpt(graph, priorDict, weightDict, df = 0.15, maxIterations = 50):
	pRankDict = {}
	graphLen = len(graph)
	uniformProbability = 1 / graphLen
	for sentenceID in range(0, len(graph)):
		pRankDict[sentenceID] = uniformProbability
	for _ in range(0, maxIterations):
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
				linkSum += linkSumNum / edgeSum
			pRankDict[node] = (discountFactor / priorSum) + ((1 - df) * linkSum)
	return pRankDict

def docSummaryEx2(document):
	if isinstance(document, str):
		documentString = getString(document)
		document = getSentences(documentString)
	invIndex = invertedIndex(document)
	graphDict = createGraph(document, invIndex)
	priorDict = nodePriorSimilarity(invIndex, document, documentString)
	weightDict = edgeWeightSimilarity(invIndex, graphDict, document)
	pRankDict = pageRankOpt(graphDict, priorDict, weightDict)
	topSentences = getTopSentences(pRankDict, document)
	return topSentences

#Summaries for exercise 1
def getPredictedSummariesEx1():
	path = './train_pt/'
	summaries = []
	for doc in os.listdir(path):
		summary = docSummaryEx1(path + doc)
		summaries.append(summary)
	return summaries

#Summaries for exercise 2
def getPredictedSummariesEx2():
	path = './train_pt/'
	summaries = []
	for doc in os.listdir(path):
		summary = docSummaryEx2(path + doc)
		summaries.append(summary)
	return summaries


def main():
	predictedSum = getPredictedSummariesEx1()
	relevantSum = getRelevantSummaries()
	MAP = map(predictedSum, relevantSum)
	print('Mean Average Precision:', MAP)

if __name__ == '__main__':
	main()