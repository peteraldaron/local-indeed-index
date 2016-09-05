#content acquirer
#using url given by a post page, visit url and try to extract anything useful
#about the post

from urllib import request
from bs4 import BeautifulSoup as BS

def parseHTTPUrl(url):
    httpData = urllib.request.urlopen(url).read()
    return BS(httpData, 'html.parser')
