#Projecto Part2

import os
from utils import getString, getSentences, getTopSentences
from utils import getRelevantSummaries, map
from utils import invertedIndex
from exercise2 import createGraph, nodePriorPosition
from exercise2 import nodePriorSimilarity, nodePriorScores, nodePriorDegree
from sklearn.linear_model import Perceptron

def getFeatures(documentString, documentSentences):
	features = []
	invIndex = invertedIndex(documentSentences)
	graph = createGraph(documentSentences, invIndex)

	priorDictSim = nodePriorSimilarity(invIndex, documentSentences, documentString)
	#priorDictDegree = nodePriorDegree(graph, documentSentences)
	priorDictPosition = nodePriorPosition(documentSentences, documentString)

	for i in range(0, len(documentSentences)):
		sentenceScore = []
		sentenceScore.append(priorDictSim[i])
		#sentenceScore.append(priorDictDegree[i])
		sentencesScore.append(priorDictPosition[i])
		features.append(sentenceScore)
	return features

def getTargets(trainSentences, testSentences):
	targets = []
	for sentence in trainSentences:
		if sentence in testSentences:
			targets.append(1)
		else:
			targets.append(0)
	return targets

def trainPerceptron():
	pathTrain = './corpus_train/train_set/'
	pathTest = './corpus_train/test_set/'
	trainDocs = os.listdir(pathTrain)
	testDocs = os.listdir(pathTest)
	classifier = Perceptron()

	for i in range(0, len(os.listdir(pathTrain))):
		trainDocString = getString(pathTrain + trainDocs[i])
		testDocString = getString(pathTest + testDocs[i])

		trainSentences = getSentences(trainDocString)
		testSentences = getSentences(testDocString)

		docFeatures = getFeatures(trainDocString, trainSentences)
		docTargets = getTargets(trainSentences, testSentences)

		classifier.partial_fit(docFeatures, docTargets, classes = [0, 1])
	return classifier

def docSummaryEx3(document, weightsList):
	if isinstance(document, str):
		documentString = getString(document)
		document = getSentences(documentString)
	invIndex = invertedIndex(document)
	graphDict = createGraph(document, invIndex)
	documentScore = {}

	#Calculate features and update sentences scores
	priorDictSim = nodePriorSimilarity(invIndex, document, documentString)
	#priorDictDegree = nodePriorDegree(invIndex, document)
	#priorDictScores = nodePriorScores(invIndex, document, documentString)
	priorDictPosition = nodePriorPosition(document, documentString)
	for node in range(0, len(document)):
		documentScore[node] = priorDictSim[node] * weightsList[0] + priorDictDegree[node] * weightsList[1] + priorDictPosition[node] * weightsList[2]

	topSentences = getTopSentences(documentScore, document)
	return topSentences

def getPredictedSummariesEx3(weightsList):
	path = './corpus_test/train_set/'
	summaries = []
	for doc in os.listdir(path):
		summary = docSummaryEx3(path + doc, weightsList)
		summaries.append(summary)
	return summaries


def main():
	classifier = trainPerceptron()
	weightsList = []
	for weight in classifier.coef_[0]:
		weightsList.append(weight)

	predictedSum = getPredictedSummariesEx3(weightsList)
	relevantSum = getRelevantSummaries()
	MAP = map(predictedSum, relevantSum)
	print('Mean Average Precision:', MAP)

if __name__ == '__main__':
	main()
