import indeed, db
from indeed import IndeedClient
import os, sys, fs


class Client:
    _singleton = None;
    def __init__(self, clientKey):
        self.client = IndeedClient(clientKey)

    def queryAll(title="software", location="", country="fi"):
        params = {
                'q' : title,
                'l' : location,
                'userip' : "8.8.8.8",
                'co' : country,
                'useragent' : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.80 Safari/537.36"
        }
        results = self.client.search(**params)
        while results.totalResults > results.end:
            #store results:
            #TODO
            params['start'] = results.end
            results = self.client.search(**params)




def getClient():
    if Client._singleton is None:
        with open("key") as fp:
            key = fp.readline()
            Client._singleton = Client(key)
    return Client._singleton



