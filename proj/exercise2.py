#Projecto Part2

from utils import getRelevantSummaries, map
from exercise1 import docSummary
import os

def prMetrics():
	return 0

def pageRankOpt(graph, df = 0.15, maxIterations = 50):
	pRankDict = {}
	graphLen = len(graph)
	uniformProbability = 1 / graphLen
	for sentenceID in range(0, len(graph)):
		pRankDict[sentenceID] = uniformProbability
	for _ in range(0, maxIterations):
		for node in graph:
			discountFactor = df / graphLen
			linkSum = 0
			for linkedNode in graph[node]:
				linkSum += pRankDict[linkedNode] / len(graph[linkedNode])
			pRankDict[node] = discountFactor + (1 - df) * linkSum
	return pRankDict

def getPredictedSummaries():
	path = os.getcwd() + '/train_pt/'
	summaries = []
	for doc in os.listdir(path):
		summary = docSummary(path + doc)
		summaries.append(summary)
	return summaries

def main():
	predictedSum = getPredictedSummaries()
	relevantSum = getRelevantSummaries()
	MAP = map(predictedSum, relevantSum)
	print(MAP)

if __name__ == '__main__':
	main()