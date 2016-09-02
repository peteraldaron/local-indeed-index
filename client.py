import indeed, db
from indeed import IndeedClient
import os, sys



#need to initialize database with client
class Client:
    _singleton = None;
    _uastring =  "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.80 Safari/537.36"
    def __init__(self, clientKey):
        self.client = IndeedClient(clientKey)
        self.db = db.DataBase();
        self.clientKey = clientKey

    def _entry_fields_cleanup(result):
        #remove useless fields:
        del result['onmousedown']
        del result['indeedApply']
        del result['formattedRelativeTime']
        del result['sponsored']
        #replace _id
        result['_id'] = result['jobkey']
        del result['jobkey']
        #convert date to actual mongo time:
#TODO: we need node-like conversion
        return result

    def queryAll(self, title="software", location="", country="fi"):
        params = {
                'q' : title,
                'l' : location,
                'co' : country,
                'userip' : '8.8.8.8',
                'useragent' : Client._uastring
        }
        results = self.client.search(**params)
        #aggregate all results first:
        aggregated_results = [];
        while 'totalResults' in results\
                and results['totalResults'] > results['end']:
            aggregated_results.extend(results['results']);
            params['start'] = results['end'];
            results = self.client.search(**params);
        #postprocessing:
        #remove expired entries:
        aggregated_results = [x for x in aggregated_results if not x['expired']]
        #cleanup entry fields:
        aggregated_results = list(map(lambda x: Client._entry_fields_cleanup(x),
                aggregated_results))

        #store results:
        if len(aggregated_results) > 0:
            self.db.insertManyIntoCollection(aggregated_results, "indeed."+country);

def getClient():
    if Client._singleton is None:
        with open("key") as fp:
            key = fp.readlines()
            key = key[0][:-1];
            Client._singleton = Client(key)
    return Client._singleton
