#content acquirer
#using url given by a post page, visit url and try to extract anything useful
#about the post

import urllib, re
from urllib import request
from bs4 import BeautifulSoup as BS
from nltk.corpus import stopwords
from nltk import wordpunct_tokenize

def parseHTTPUrl(url):
    httpData = urllib.request.urlopen(url).read()
    return BS(httpData, 'html.parser')

#detect language of string
#return most probable language string
#with the list of frequencies(probabilities)
def languageDetect(string):
    tokens = [x.lower() for x in wordpunct_tokenize(string)]
    frequencies = sorted(
            map(lambda lang:
                    (lang, sum([1 for x in tokens if x in set(stopwords.words(lang))])),
                stopwords.fileids()),
            key=lambda x: x[1],
            reverse=True)

    return frequencies[0][0], frequencies

def getJobSummaryOfUrl(url):
    rawtext = parseHTTPUrl(url).find(id="job_summary").get_text()
    re.sub(r'[\r\t\n]', ' ', rawtext)
    return rawtext

def getLanguageOfJobSummary(url):
    return languageDetect(getJobSummaryOfUrl(url))
