#Projecto Part2

#import xml.etree.ElementTree as ET

from xml.etree import cElementTree as ET
xmlstr = """
    <root>
    <page>
    <title>Chapter 1</title>
    <content>Welcome to Chapter 1</content>
    </page>
    <page>
    <title>Chapter 2</title>
    <content>Welcome to Chapter 2</content>
    </page>
    </root>
    """
root = ET.fromstring(xmlstr)
#root = ET.fromstring(xmlstr)
for item in list(root):
    title = item.find('items:title')
    #    name = item.get('name')
    print(item.text)
#print(title, name)
#title = page.find('title').text
#content = page.find('descritption').text
#print(title)
