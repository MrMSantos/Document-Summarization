#Projecto Part2

from utils import getRelevantSummaries, getGreedySummaries, calculateMetrics

def prMetrics():

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


def main():
	documentString = getString('file_english.txt')
	sentencesList = getSentences(documentString)
	graphDict = createGraph('file_english.txt')
	pRankDict = pageRank(graphDict)

	relevantSum = getRelevantSummaries()
	MAP = calculateMetrics(relevantSum, predictedSum)

if __name__ == '__main__':
	main()