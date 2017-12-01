#Projecto Part2

from exercise1 import docSummary
from utils import getSentences
from xml.etree import cElementTree as ET
import re
import os

def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext.strip()

def getLinkFromXML(file):
    tree = ET.parse(file)
    root = tree.getroot()
    for items in root.iter('item'):
        link = items.find('link').text
        print(link)

def getSentencesfromXML(file, language = 'english'):
    sentences = []
    tree = ET.parse(file)
    root = tree.getroot()
    for items in root.iter('item'):
        #TITLE
        title = items.find('title').text
        if title != None:
            titleSentences = getSentences(title, language)
            sentences += titleSentences
        #DESCRIPTION
        description = items.find('description').text
        descriptionClean = cleanhtml(description)
        descriptionSentences = getSentences(cleanhtml(descriptionClean), language)
        sentences += descriptionSentences
        
    return sentences

#getLinkFromXML('Washington_Post.xml')

def main():
    fileSentences = []
    for file in os.listdir(os.getcwd()):
        if file.endswith('.xml') or file.endswith('.rss'):
            fileSentences += getSentencesfromXML(file)
    summary = docSummary(fileSentences)
    print(summary)

if __name__ == '__main__':
    main()