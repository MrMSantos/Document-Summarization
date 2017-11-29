#Projecto Part2

from utils import getString, getSentences
from utils import docSimilarity, docSummary

#OPTIMIZE INVERTED TABLE
def createGraph(document, threshold = 0.2):
	graphDict = {}
	docString = getString(document)
	sentenceList = getSentences(docString, 'english')
	for sentenceID in range(0, len(sentenceList)):
		graphDict[sentenceID] = []

	for sentenceID in range(0, len(sentenceList)):
		similarityList = docSimilarity(sentenceList, sentenceList[sentenceID])
		for similarityID in range(0, len(similarityList)):
			if similarityList[similarityID] > threshold and sentenceID != similarityID:
				graphDict[sentenceID].append(similarityID)
	return graphDict

#VERIFICAR SE OS VALORES SE ALTERARAM A CADA ITERAÇÃO
def pageRank(graph, df = 0.15, maxIterations = 50):
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
	print(pRankDict)
	return pRankDict


def main():
	documentString = getString('file_english.txt')
	sentencesList = getSentences(documentString)
	graphDict = createGraph('file_english.txt')
	pRankDict = pageRank(graphDict)
	topSentences = docSummary(pRankDict, sentencesList, sort = True)
	for sent in topSentences: print(sent)

if __name__ == '__main__':
	main()