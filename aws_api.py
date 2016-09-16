'''
Created on Sep 12, 2016

@author: Devin
'''
import urllib, requests, os
import argparse, json
import ConfigParser

class SimpleCurl:
    def __init__(self, 
                 endpoint,
                 api_key,
                 s3_path, 
                 json_file):
        self.api_key = api_key
        self.endpoint = endpoint
        self.json_file = json_file
        self.s3_path = s3_path

    def get(self):
        url = os.path.join(self.endpoint, urllib.quote(self.s3_path, safe=''))
        print 'Getting from: {}'.format(url)
        resp = requests.get(url=url, headers={'Content-Type': 'application/json', 'x-api-key': self.api_key})
        print resp, resp.content

    def patch(self):
        url = os.path.join(self.endpoint, urllib.quote(self.s3_path, safe=''))
        with open(self.json_file, 'r') as f:
            json_str = f.read()
        out = json.loads(json_str)
        print 'Patching to: {}'.format(url)
        resp = requests.patch(url=url, data=json.dumps(out), headers={'Content-Type': 'application/json', 'x-api-key': self.api_key})
        print resp, resp.content

if __name__ == '__main__':
    config = ConfigParser.ConfigParser()    
    config.read('api_config.conf')
    endpoint = config.get('Info', 'endpoint')
    api_key = config.get('Info', 'api_key')

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', help='Example S3 Path')
    parser.add_argument('-o', help='Operation')
    parser.add_argument('-j', help='JSON file for POST/PATCH')
    args = parser.parse_args()
    curl = SimpleCurl(endpoint=endpoint, api_key=api_key, s3_path=args.p, json_file=args.j)
    getattr(curl, args.o)()
