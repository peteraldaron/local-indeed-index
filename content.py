#content acquirer
#using url given by a post page, visit url and try to extract anything useful
#about the post

import urllib, re, asyncio, threading
from urllib import request
from bs4 import BeautifulSoup as BS
from nltk.corpus import stopwords
from nltk import wordpunct_tokenize

_stopWordsDict = None;
_popevent = threading.Event()
#stopwords set initializer:
def getStopWords():
    global _stopWordsDict
    global _popevent

    if _stopWordsDict is None and not _popevent.is_set():
        try:
            _stopWordsDict = {}

            for lang in stopwords.fileids():
                _stopWordsDict[lang] = set(stopwords.words(lang))

        except Exception as e:
            print("error in getStopWords:"+e)

        finally:
            _popevent.set()

    _popevent.wait()
    return _stopWordsDict


def parseHTTPUrl(url):
    httpData = urllib.request.urlopen(url).read()
    return BS(httpData, 'html.parser')

#detect language of string
#return most probable language string
#with the list of frequencies(probabilities)
def languageDetect(string):
    tokens = [x.lower() for x in wordpunct_tokenize(string)]
    stopwordsDict = getStopWords()
    try:
        frequencies = sorted(
                map(lambda lang:
                        (lang, sum([1 for x in tokens if x in stopwordsDict[lang]])),
                    stopwords.fileids()),
                key=lambda x: x[1],
                reverse=True)

    except Exception as e:
        print(stopwordsDict)
        print("exception in landet" + e)

    return frequencies[0][0], frequencies


def getJobSummary(url):
    rawtext = parseHTTPUrl(url).find(id="job_summary").get_text()
    re.sub(r'[\r\t\n]', ' ', rawtext)
    return rawtext

def getLanguageOfJobSummary(url):
    return languageDetect(getJobSummaryOfUrl(url))
