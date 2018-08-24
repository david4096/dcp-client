#!/usr/local/bin/python3.6
import requests
import json

class Client:
    '''
    Expose requests methods while simplifying DCP auth.
    '''
    def __init__(self, base_url="https://dcp.bionimbus.org", credentials_filename="credentials.json"):
        self.base_url = base_url
        self.access_token = self.get_access_token(
            credentials_filename)
        self.sheepdog_path = 'api/v0/submission'
        self.indexd_path = 'index/index/'
        self.download_path = 'user/data/download'
        self.peregrine_path = '' # TODO ...
    
    def headers(self, headers={}):
        '''
        Return the headers dict that includes the access token for 
        creating a request.
        '''
        # TODO token refreshing
        headers.update({'Authorization': 'bearer ' + self.access_token})
        return headers
    
    def get_access_token(self, filename):
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
       Exposes an authorized form of requests get and extends the 
       headers keyword to include an Authorization bearer token.
       '''
       return requests.get(
            "{}/{}".format(self.base_url, base_path),
            headers=self.headers(kwargs.get('headers', {})),
            *kwargs)
    
    def post(self, base_path, **kwargs):
        '''
        Exposes the post feature of the requests module adding a bearer token.
        '''
        return requests.post(
            "{}/{}".format(self.base_url, base_path),
            headers=self.headers(kwargs.get('headers', {})),
            *kwargs)

    def get_download_url(self, guid):
        '''
        Accepts a data guid and returns a signed URL at which the guid can
        be downloaded (if auth concerns are met).
        '''
        try:
            response = self.get('{}/{}'.format(self.download_path, guid)).json()['url']
        except Exception as e:
            print('Failed to get download URL')
            print(str(e))
            return None
        return response
