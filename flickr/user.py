"""User functions"""

import logging
from flickr import api

log = logging.getLogger(__name__)


def get_id(username):
    payload = {
        'method': 'flickr.people.findByUsername',
        'username': username,
    }
    log.info(f'Getting user_id for {username}')
    return api.call(payload)[0]['nsid']


def get_photos(user_id):
    """Returns list of photo dicts"""
    payload = {
        'extras': 'date_taken, tags, title, url_o, url_q, views',
        'method': 'flickr.photos.search',
        'user_id': user_id}
    photos = []
    log.info(f'Getting photos for user {user_id}')
    for response in api.call(payload):
        for photo in response['photo']:
            photos.append(photo)
    return photos


def get_photosets(user_id):
    """Get list of photosets"""
    payload = {
        'method': 'flickr.photosets.getList',
        'user_id': user_id,
    }
    data = []
    log.info(f'Getting photosets for user {user_id}')
    for photosets in api.call(payload):
        for photoset in photosets['photoset']:
            data.append(photoset)
    return data
