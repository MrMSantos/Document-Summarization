#Projecto Part2

from xml.etree import cElementTree as ET

tree = ET.parse('CNN.rss')
root = tree.getroot()

for items in root.iter('item'):
    title = items.find('title').text
    description = items.find('description').text
    print('TITLE:', title)
    print('DESCRIPTION:', description)