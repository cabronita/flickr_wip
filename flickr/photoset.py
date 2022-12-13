"""Album (photoset) functions"""

import logging
from flickr import api, db
from flickr.photo import save

log = logging.getLogger(__name__)


def download(photoset_id):
    """Download photos from photoset"""
    print(f"Processing {photoset_id}")
    photos = get_photos(photoset_id)
    if not photos:
        return
    user_id = get_info(photoset_id)['owner']
    print(f"https://www.flickr.com/photos/{user_id}/albums/{photoset_id}")
    downloaded_photos = db.load_downloaded_photos()
    for photo in photos:
        if int(photo['id']) in downloaded_photos:
            log.info(f'Skipping download of {photo["id"]}')
        else:
            datetaken = photo['datetaken']
            url = photo['url_o'] if 'url_o' in photo else None
            save(datetaken, photo['id'], str(photoset_id), url)


def get_info(photoset_id):
    payload = {
        'method': 'flickr.photosets.getInfo',
        'photoset_id': photoset_id}
    log.info(f'Getting info for photoset {photoset_id}')
    try:
        return api.call(payload)[0]
    except ValueError as e:
        log.warning(f'{photoset_id} {e}')
        return None


def get_photos(photoset_id):
    """Return list of photos in album"""
    payload = {
        'extras': 'date_taken, tags, title, url_o, url_q, views',
        'method': 'flickr.photosets.getPhotos',
        'photoset_id': photoset_id}
    photos = []
    log.info(f'Getting photos in {photoset_id}')
    try:
        api_call = api.call(payload)
    except ValueError as e:
        log.warning(f'{photoset_id} {e}')
        return None
    for element in api_call:
        for photo in element['photo']:
            photos.append(photo)
    return photos
