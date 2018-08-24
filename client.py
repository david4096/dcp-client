#!/usr/local/bin/python3.6
import requests
import json

class Client:
    '''
    Export JSON following the DCP metadata including a 
    manifest of all files and any available URL data.
    '''
    def __init__(self, credentials_filename, base_url):
        self.base_url = base_url
        self.access_token = self.access_token(
            credentials_filename)
        self.sheep_url = '{}/api/v0/submission'.format(base_url)
        self.indexd_url = '{}/index/index/'.format(base_url)
    
    def headers(self, headers={}):
        '''
        Return the headers dict that includes the access token for 
        creating a request.
        '''
        headers.update({'Authorization': 'bearer ' + self.access_token})
        return headers
    
    def access_token(self, filename):
        '''
        Get a fence access token using a path to a credentials.json
        and return that token.
        '''
        auth_url = '{}/user/credentials/cdis/access_token'.format(self.base_url)
        print('Using {} to get an access token.'.format(filename))
        try:
            json_data = open(filename).read()
            keys = json.loads(json_data)
        except Exception as e:
            print('Failed to find your credentials! Check your credentials path: {} \n {}'.format(filename, str(e)))
            return None
        print('Getting access token from {} .'.format(auth_url))
        try:
            access_token = requests.post(auth_url, json=keys).json()['access_token']
        except Exception as e:
            print('Failed to authenticate! Check the URL {} \n {}'.format(auth_url, str(e)))
            return None
        return access_token

    def get(self, base_path, **kwargs):
       '''
       Exposes an authorized form of requests get
       '''
       return requests.get(
            "{}/{}".format(self.base_url, base_path),
            headers=self.headers(),
            *kwargs)
