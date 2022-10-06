"""Group functions"""

import logging
from flickr import api

log = logging.getLogger(__name__)


def get_pool_size(group_id):
    """Get number of photos in the group pool"""
    payload = {
        'method': 'flickr.groups.getInfo',
        'group_id': group_id}
    log.info(f'Getting info for group {group_id}')
    return int(api.call(payload)[0]['pool_count']['_content'])
