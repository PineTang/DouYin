from douyin.handlers import Handler
from motor.motor_asyncio import AsyncIOMotorClient
from douyin.structures import *


class MongoHandler(Handler):
    
    def __init__(self, host='localhost', port=27017, username=None, password=None, db='douyin'):
        """
        init save folder
        :param folder:
        """
        super().__init__()
        # self.folder = folder
        # if not exists(self.folder):
        #     makedirs(self.folder)
        self.client = AsyncIOMotorClient(host=host, port=port, username=username, password=password)
        self.db = self.client[db]
    
    async def process(self, obj, **kwargs):
        """
        download to file
        :param url: resource url
        :param name: save name
        :param kwargs:
        :return:
        """
        collection_name = 'default'
        if isinstance(obj, Video):
            collection_name = 'videos'
        elif isinstance(obj, Music):
            collection_name = 'musics'
        collection = self.db[collection_name]
        # save to mongodb
        print('Saving', obj, 'to mongodb...')
        if await collection.update_one({'id': obj.id}, {'$set': obj.json()}, upsert=True):
            print('Saved', obj, 'to mongodb successfully')
        else:
            print('Error occurred while saving', obj)
