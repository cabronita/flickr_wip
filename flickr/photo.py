"""Photo functions"""

import logging
import requests
from flickr import api

log = logging.getLogger(__name__)


def download(photo_id):
    """Download photo"""
    details = get_info(photo_id)
    datetaken = details['dates']['taken']
    url = get_max_size_url(photo_id)
    timestamp = f'{datetaken}'.replace(' ', '_').replace(':', '')
    filename = f'{timestamp},{photo_id}.jpg'
    log.info(f'Downloading {photo_id} {url}')
    response = requests.get(url)
    log.info(f'Saving {filename}')
    with open(filename, 'wb') as file:
        file.write(response.content)


def get_info(photo_id):
    """Get photo details"""
    log.info(f'Getting details of photo {photo_id}')
    payload = {
        'method': 'flickr.photos.getInfo',
        'photo_id': photo_id,
    }
    return api.call(payload)[0]


def get_max_size_url(photo_id):
    """Get url to the largest photo available"""
    log.info(f'Getting max size for {photo_id}')
    payload = {
        'method': 'flickr.photos.getSizes',
        'photo_id': photo_id,
    }
    sizes = api.call(payload)[0]['size']
    return sorted(sizes, key=lambda x: x['width'])[-1]['source']
