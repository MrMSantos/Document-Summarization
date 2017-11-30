#Projecto Part2

from utils import getString, getSentences, getTopSentences
from utils import docSimilarity

#OPTIMIZE INVERTED TABLE
def createGraph(sentenceList, threshold = 0.2):
	graphDict = {}
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
	return pRankDict

#ORDER ATTRIBUTE
def docSummary(file, ordered = False):
	documentString = getString(file)
	sentencesList = getSentences(documentString)
	graphDict = createGraph(sentencesList)
	pRankDict = pageRank(graphDict)
	topSentences = getTopSentences(pRankDict, sentencesList, ordered)
	return topSentences

def docSummary4(sentencesList, ordered = False):
	graphDict = createGraph(sentencesList)
	pRankDict = pageRank(graphDict)
	topSentences = getTopSentences(pRankDict, sentencesList, ordered)
	return topSentences

def main():
	summary = docSummary('file_english.txt', ordered = True)
	print('---- Summary for document file_english.txt ----')
	for sent in summary: print(sent)

if __name__ == '__main__':
	main()