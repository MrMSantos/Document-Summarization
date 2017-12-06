#Projecto Part2

import os
from utils import getString, getSentences
from utils import invertedIndex
from exercise2 import nodePriorSimilarity
from sklearn.linear_model import Perceptron

def getFeatures(documentString, documentSentences):
	features = []
	invIndex = invertedIndex(documentSentences)
	priorDict = nodePriorSimilarity(invIndex, documentSentences, documentString)
	for i in range(0, len(priorDict)):
		features.append([priorDict[i]])
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


def main():
	classifier = trainPerceptron()

if __name__ == '__main__':
	main()