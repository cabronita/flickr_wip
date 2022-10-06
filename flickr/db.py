"""Internal database operations"""

import logging
import pymongo

log = logging.getLogger(__name__)


def get_client():
    replica_set = 'mongodb://mongo1:27017,mongo2:27017,mongo3:27017/?replicaSet=rs0'
    db = 'flickr'
    return pymongo.MongoClient(replica_set)[db]


def load_secrets():
    client = get_client()
    collection = client['apps']
    log.info('Checking if secrets present in database')
    if collection.count_documents({'_id': 'flickr'}):
        log.info('Loading secrets from database')
        return collection.find_one({'_id': 'flickr'})['secrets']


def save_secrets(secrets):
    client = get_client()
    collection = client['apps']
    log.info('Saving secrets to database')
    collection.insert_one({'_id': 'flickr', 'secrets': secrets})
