#Projecto Part2

from exercise1 import docSummary
from utils import getSentences
from xml.etree import cElementTree as ET
import re
import os

begin = """<!DOCTYPE html>
    <html lang="en">
    
    <head>
    
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="">
    <meta name="author" content="">
    
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
    <h1 style="color: #fff">Summarys</h1>
    <br>
    <h4 style="color: #fff; font-weight: lighter;">Processamento e Recuperação de Informação</h4>
    </div>
    </div>
    </header>
    
    <!-- Page Content -->
    <div class="container">
    
    <hr class="featurette-divider">
    """

end= """
    </div>
    
    <hr class="featurette-divider">
    
    <!-- Footer -->
    <footer>
    <div class="row"  style="background-color:">
    <div class="col-lg-12">
    <p class="lead" align="center">Made by Group 23</p>
    </div>
    </div>
    </footer>
    
    </div>
    <!-- /.container -->
    
    <!-- jQuery -->
    <script src="js/jquery.js"></script>
    
    <!-- Bootstrap Core JavaScript -->
    <script src="js/bootstrap.min.js"></script>
    
    </body>
    
    </html>
    """

link_begin= """
    <!-- First Featurette -->
    <div class="featurette" id="about">
    <h2 class="featurette-heading">Summary</h2>
    <br>
    <p class="lead size-text"><a href="
    """
link_end= """
    ">
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
    for file in os.listdir(os.getcwd()):
        if file.endswith('.xml') or file.endswith('.rss'):
            tree = ET.parse(file)
            root = tree.getroot()
            for items in root.iter('item'):
                title = items.find('title').text
                description = items.find('description').text
                if((title != None and sentence in title) or sentence in description):
                    return items.find('link').text
    return;

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

def CheckUserExists(user):
    with open("C:/~/database.txt", 'r') as file:
        if re.search('^{0}$'.format(re.escape(user)), file.read(), flags=re.M):
            return True
        else:
            return False

def main():
    fileSentences = []
    f = open('summary.html','w')
    message = begin
    for file in os.listdir(os.getcwd()):
        if file.endswith('.xml') or file.endswith('.rss'):
            fileSentences += getSentencesfromXML(file)
    summary = docSummary(fileSentences)
    for sum in summary:
        link = getLinkFromXML(sum)
        message += (link_begin + link + link_end + sum + text)
    message += end
    print(message)
    f.write(message)
    f.close()

if __name__ == '__main__':
    main()
