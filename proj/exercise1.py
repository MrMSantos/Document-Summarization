#Projecto Part2

from utils import getString, getSentences, getTopSentences
from utils import invertedIndex, docSimilarity

#OPTIMIZE INVERTED TABLE
def createGraph(sentenceList, invIndex, threshold = 0.15):
	graphDict = {}
	for sentenceID in range(0, len(sentenceList)):
		graphDict[sentenceID] = []

	for sentenceID in range(0, len(sentenceList)):
		similarityList = docSimilarity(invIndex, sentenceList, [sentenceList[sentenceID]])
		for similarityID in range(0, len(similarityList)):
			if similarityList[similarityID] > threshold and sentenceID != similarityID:
				graphDict[sentenceID].append(similarityID)
	
	if all(len(graphDict[node]) == 0 for node in graphDict):
		return graphDict

	newGraphDict = {}
	for node in graphDict:
		if len(graphDict[node]) != 0:
			newGraphDict[node] = graphDict[node]
	return newGraphDict

def pageRank(graph, df = 0.15, maxIterations = 50):
	pRankDict = {}
	graphLen = len(graph)
	uniformProbability = 1 / graphLen
	discountFactor = df / graphLen
	updateDF = 1 - df
	for node in graph:
		pRankDict[node] = uniformProbability
	
	for _ in range(0, maxIterations):
		auxDict = {}
		for node in graph:
			linkSum = 0
			for linkedNode in graph[node]:
				linkSum += pRankDict[linkedNode] / len(graph[linkedNode])
			auxDict[node] = discountFactor + updateDF * linkSum
		pRankDict = auxDict
	return pRankDict

def docSummaryEx1(document, ordered = False, language = 'portuguese'):
	if isinstance(document, str):
		documentString = getString(document)
		document = getSentences(documentString, language)
	invIndex = invertedIndex(document)
	graphDict = createGraph(document, invIndex)
	pRankDict = pageRank(graphDict)
	topSentences = getTopSentences(pRankDict, document, ordered)
	return topSentences


def main():
	summary = docSummaryEx1('./train_en/file_english.txt', ordered = True, language = 'english')
	print('---- Summary for document file_english.txt ----')
	for sent in summary: print(sent)

if __name__ == '__main__':
	main()