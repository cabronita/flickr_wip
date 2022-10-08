"""Album (photoset) functions"""

import logging
import requests
from flickr import api, db
from flickr.photo import get_max_size_url

log = logging.getLogger(__name__)


def download(photoset_id):
    """Download photos from photoset"""
    photos = get_photos(photoset_id)
    downloaded_photos = db.load_downloaded_photos()
    for photo in photos:
        if int(photo['id']) in downloaded_photos:
            print(f'Skipping download of {photo["id"]}')
        else:
            datetaken = photo['datetaken']
            if 'url_o' in photo.keys():
                url = photo['url_o']
            else:
                url = get_max_size_url(photo['id'])
            timestamp = f'{datetaken}'.replace(' ', '_').replace(':', '')
            filename = f'{timestamp},{photo["id"]}.jpg'
            log.info(f'Downloading {photo["id"]} {url}')
            response = requests.get(url)
            log.info(f'Saving {filename}')
            with open(filename, 'wb') as file:
                file.write(response.content)
            db.save_downloaded_photo(photo['id'])


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
