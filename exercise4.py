#Projecto Part2
from utils import getSentences
from xml.etree import cElementTree as ET
import re

def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext.strip()


def getAllSentences():
    sentences = []
    tree = ET.parse('New_York_Times.xml')
    root = tree.getroot()
    for items in root.iter('item'):
        #TITLE
        title = items.find('title').text
        titleSentences = getSentences(title)
        sentences += titleSentences
        
        #DESCRIPTION
        description = items.find('description').text
        descriptionClean = cleanhtml(description)
        descriptionSentences = getSentences(cleanhtml(descriptionClean))
        sentences += descriptionSentences
        
        #print('TITLE:', title)
        #print('DESCRIPTION:', description)
    print(sentences)
    return sentences

def main():
    getAllSentences()


main()
