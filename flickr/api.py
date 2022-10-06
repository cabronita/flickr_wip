"""Internal API operations"""

import logging
import requests_oauthlib
import sys
import time
from flickr import db

log = logging.getLogger(__name__)


def generate_secrets():
    """Perform OAuth and return keys and secrets"""
    print('Secrets not found. Generating new secrets')
    request_token_url = 'https://www.flickr.com/services/oauth/request_token'
    base_authorization_url = 'https://www.flickr.com/services/oauth/authorize'
    access_token_url = 'https://www.flickr.com/services/oauth/access_token'
    callback_uri = 'oob'
    client_key = input('Enter your API key: ')
    client_secret = input('Enter your API secret: ')

    print('1) Getting request token.')
    request_token = requests_oauthlib.OAuth1Session(client_key, client_secret, callback_uri=callback_uri)
    fetch_response = request_token.fetch_request_token(request_token_url)
    resource_owner_key = fetch_response.get('oauth_token')
    resource_owner_secret = fetch_response.get('oauth_token_secret')

    print('2) Getting authorization.', end=' ')
    authorization_url = request_token.authorization_url(base_authorization_url)
    print('Authorize and get access code here:')
    print(f'{authorization_url}&perms=read')
    verifier = input('then paste the access code: ')

    print('3) Exchanging request token for access token.')
    oauth = requests_oauthlib.OAuth1Session(client_key, client_secret, resource_owner_key, resource_owner_secret,
                                            verifier=verifier)
    oauth_tokens = oauth.fetch_access_token(access_token_url)
    resource_owner_key = oauth_tokens.get('oauth_token')
    resource_owner_secret = oauth_tokens.get('oauth_token_secret')

    return {'client_key': client_key,
            'client_secret': client_secret,
            'resource_owner_key': resource_owner_key,
            'resource_owner_secret': resource_owner_secret}


def _get_oa1_session():
    secrets = db.load_secrets()
    if secrets is None:
        secrets = generate_secrets()
        db.save_secrets(secrets)
    oa1_session = requests_oauthlib.OAuth1Session(
        secrets['client_key'],
        secrets['client_secret'],
        secrets['resource_owner_key'],
        secrets['resource_owner_secret'])
    return oa1_session


_session = _get_oa1_session()


def call(payload):
    """Call Flickr API"""
    response = None
    response_list = []
    page = 1
    data = {}
    errors, retry_count = 0, 1
    while True:
        payload.update({
            'format': 'json',
            'nojsoncallback': 1,
            'page': page,
            'per_page': 500})
        while response is None:
            try:
                log.info(f'Calling {payload["method"]}, page {page}')
                response = _session.get('https://www.flickr.com/services/rest/', params=payload).json()
                for key in response.keys():
                    if key != 'stat':  # There are only 2 keys. We ignore 'stats'.
                        data = response[key]
                        response_list.append(data)
            except ValueError:
                log.warning('API call failed and will be re-tried')
                errors += 1
                if errors > retry_count:
                    sys.exit(2)
                time.sleep(1)
        if response['stat'] != 'ok':
            raise ValueError(response['message'])
        if 'page' not in data:  # If response is a single-page one
            break
        response = None
        if int(data['page']) < int(data['pages']):
            page += 1
        else:
            break
    return response_list
