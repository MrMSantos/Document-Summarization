#Projecto Part2
from utils import getSentences
from xml.etree import cElementTree as ET
import re
import os

def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext.strip()


def getSentencesfromXML(file):
    sentences = []
    tree = ET.parse(file)
    root = tree.getroot()
    for items in root.iter('item'):
        #TITLE
        title = items.find('title').text
        if title != None:
            titleSentences = getSentences(title)
            sentences += titleSentences
        
        #DESCRIPTION
        description = items.find('description').text
        descriptionClean = cleanhtml(description)
        descriptionSentences = getSentences(cleanhtml(descriptionClean))
        sentences += descriptionSentences
        
    return sentences

def main():
    fileSentences = []
    for file in os.listdir(os.getcwd()):
        print(file)
        if file.endswith('.xml') or file.endswith('.rss'):
            fileSentences += getSentencesfromXML(file)
    print(fileSentences)

if __name__ == '__main__':
    main()