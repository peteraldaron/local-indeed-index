import os, pymongo
from pymongo import MongoClient

class DataBase:
    def __init__(self, dbName='indeed', port=27017, host='localhost'):
        #definitions:
        self.dbName = dbName;
        self.port = port;
        self.host = host;
        #set up:
        self.db = self.getDataBase();

    def getDataBase(self):
        client = MongoClient(self.host, self.port);
        return client[self.dbName];

    def getCollection(self, collectionName):
        if self.db == None:
            self.db = self.getDataBase();
        return self.db[collectionName];

    def insertOneToCollection(self, document, collectionName, collection=None):
        if collection == None:
            collection = self.getCollection(collectionName);
        return collection.insert_one(document);

    def upsertOneToCollection(self, document, query, collectionName, collection=None):
        if collection == None:
            collection = self.getCollection(collectionName);
        return collection.find_and_modify(query, update=document, upsert=True)

    def insertManyIntoCollection(self, documents, collectionName,
            collection=None, insertNewOnly=True, insertionFilterParam="_id"):

        if collection == None:
            collection = self.getCollection(collectionName);

        #filter out any preexisting entries:
        existingDocs = self.findExistingEntriesInCollection(documents,
                insertionFilterParam, collectionName, collection)

        if existingDocs.count() > 0:
            #aggregate existing docs by search param:
            existingDocs = set([x[insertionFilterParam] for x in
                existingDocs])

            if not insertNewOnly:
                #also update existingDocs:
                documentsToUpdate = [x for x in documents if
                        x[insertionFilterParam] in existingDocs]

                self.updateManyByParamInCollection(documentsToUpdate,
                        insertionFilterParam, collectionName, collection)

            #filter:
            documents = [x for x in documents if x[insertionFilterParam] not
                    in existingDocs]


        if len(documents) <= 0:
            return

        return collection.insert_many(documents)

    def updateManyByParamInCollection(self, documents, param, collectioNname, collection=None):
        if collection == None:
            collection = self.getCollection(collectionName);

        for doc in documents:
            collection.find_one_and_update(
                    {param : doc[param]},
                    {"$set": doc})
    '''
    returns list of entries with search param fields
    '''
    def findExistingEntriesInCollection(self, documents, searchParameter,
            collectionName, collection=None):
        if collection == None:
            collection = self.getCollection(collectionName);

        #aggregate documents of search param:
        searchCriteria = [x[searchParameter] for x in documents]
        return collection.find({
            searchParameter: {
                "$in" : searchCriteria
            }
        })
