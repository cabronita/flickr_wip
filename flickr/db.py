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


def load_downloaded_photos():
    client = get_client()
    collection = client['downloaded']
    photo_ids = []
    for photo_id in collection.find():
        photo_ids.append(photo_id['_id'])
    return photo_ids


def save_downloaded_photo(photo_id):
    client = get_client()
    collection = client['downloaded']
    try:
        collection.insert_one({'_id': photo_id})
    except pymongo.errors.DuplicateKeyError:
        log.info(f'{photo_id} already in database.')
