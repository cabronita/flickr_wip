"""User functions"""

import logging
from flickr import api, db
from flickr.photo import save

log = logging.getLogger(__name__)


def download(user_id):
    """Download user's photos"""
    print(f"Processing {user_id}")
    try:
        profileurl = get_info(user_id)['profileurl']['_content']
    except ValueError as e:
        log.warning(f'{user_id} {e}')
        return None
    print(get_info(user_id)['profileurl']['_content'])
    photos = get_photos(user_id)
    downloaded_photos = db.load_downloaded_photos()
    for photo in photos:
        if int(photo['id']) in downloaded_photos:
            log.info(f'Skipping download of {photo["id"]}')
        else:
            datetaken = photo['datetaken']
            url = photo['url_o'] if 'url_o' in photo else None
            save(datetaken, photo['id'], str(user_id), url)


def get_id(username):
    payload = {
        'method': 'flickr.people.findByUsername',
        'username': username,
    }
    log.info(f'Getting user_id for {username}')
    return api.call(payload)[0]['nsid']


def get_info(user_id):
    payload = {
        'method': 'flickr.people.getInfo',
        'user_id': user_id}
    log.info(f'Getting info for user {user_id}')
    return api.call(payload)[0]


def get_photos(user_id):
    """Returns list of photo dicts"""
    payload = {
        'extras': 'date_taken, tags, title, url_o, url_q, views',
        'method': 'flickr.photos.search',
        'user_id': user_id}
    log.info(f'Getting photos for user {user_id}')
    try:
        response = api.call(payload)
    except ValueError as e:
        log.warning(f'{user_id} {e}')
        return None
    photos = []
    for photo in response[0]['photo']:
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
    response = api.call(payload)
    for photosets in response:
        for photoset in photosets['photoset']:
            data.append(photoset)
    return data
