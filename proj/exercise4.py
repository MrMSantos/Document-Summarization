#Projecto Part2

from exercise1 import docSummaryEx1
from utils import getSentences
from xml.etree import cElementTree as ET
import re
import os

begin = """<!DOCTYPE html>
    <html lang="en">
    
    <head>
    
    <meta charset="utf-8">
    <title>Processamento e Recuperação de Informação</title>
    
    <!-- Bootstrap Core CSS -->
    <link href="css/bootstrap.min.css" rel="stylesheet">
    
    <!-- Custom CSS -->
    <link href="css/one-page-wonder.css" rel="stylesheet">
    
    </head>
    <body>
    <!-- Full Width Image Header -->
    <header class="header-image">
    <div class="headline">
    <div class="container">
    <h1 style="color: #fff">Daily World News</h1>
    <br>
    <h4 style="color: #fff; font-weight: lighter;">News from CNN, LA Times, NY Times and Washington Post</h4>
    </div>
    </div>
    </header>

    <div class="container">
    <h2 class="featurette-heading">Relevant Articles</h2>
    <hr class="featurette-divider">
    """

end = """
    </div>
    <footer>
    <div class="row"  style="background-color:">
    <div class="col-lg-12">
    <p class="lead" align="center">Made by Group 23</p>
    </div>
    </div>
    </footer>
    
    </div>

    <script src="js/jquery.js"></script>

    <script src="js/bootstrap.min.js"></script>
    
    </body>
    
    </html>
    """

link_begin = """
    <div class="featurette" id="about">
    <br>
    <p class="lead size-text"><a href="
    """
link_end = """
    " target="_blank">
    """
text = """
    </a>
    </p>
    </div>
    
    <hr class="featurette-divider">
    
    """

def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext.strip()

def getLinkFromXML(sentence):
    path = './news_xml/'
    for file in os.listdir(path):
        if file.endswith('.xml') or file.endswith('.rss'):
            tree = ET.parse(path + file)
            root = tree.getroot()
            for items in root.iter('item'):
                title = items.find('title').text
                description = items.find('description').text
                if ((title != None and sentence in title) or sentence in description):
                    return items.find('link').text

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

def main():
    fileSentences = []
    f = open('./exercise4_html/summary.html', 'w')
    message = begin
    path = './news_xml/'
    for file in os.listdir(path):
        if file.endswith('.xml') or file.endswith('.rss'):
            fileSentences += getSentencesfromXML(path + file)
    summary = docSummaryEx1(fileSentences)
    for sum in summary:
        link = getLinkFromXML(sum)
        message += (link_begin + link + link_end + sum + text)
    message += end
    f.write(message)
    f.close()

if __name__ == '__main__':
    main()
