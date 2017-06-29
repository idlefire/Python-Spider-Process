from pymongo import MongoClient

class MongoClient:

    def __init__(self, client=None):
        self.client = MongoClient('localhost', 27017) if client is None else client
        self.db = self.client.cache

    def __getitem__(self, url):
        record = self.db.webpage.find_one({'_id': url})
        if record:
            return record['result']
        else:
            raise KeyError(url + ' does not exists')

    def __setitem__(self, url, result):
        record = {'result': result}
        self.db.webpage.update({'_id': url}, record, upsert=True)
