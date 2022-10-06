"""Album (photoset) functions"""

import logging
from flickr import api

log = logging.getLogger(__name__)


def get_photos(photoset_id):
    """Return list of photos in album"""
    payload = {
        'extras': 'date_taken, tags, title, url_o, url_q, views',
        'method': 'flickr.photosets.getPhotos',
        'photoset_id': photoset_id}
    photos = []
    log.info(f'Getting photos in {photoset_id}')
    for element in api.call(payload):
        for photo in element['photo']:
            photos.append(photo)
    return photos
