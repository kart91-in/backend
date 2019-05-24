import json

import requests


class BaseCrawler(object):

    default_headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    @property
    def session(self):
        if not hasattr(self, '_session'):
            self._session = requests.Session()
        return self._session

    def json(self, text):
        return json.loads(text)

    def post(self, url, params=None, data=None, headers=None):
        headers = headers or {}
        params = params or {}
        data = data or {}
        return self.session.post(url, params=params, data=data, headers={**self.default_headers, **headers})

    def get(self, url, params=None, headers=None):
        headers = headers or {}
        params = params or {}
        return self.session.get(url, params=params, headers={**self.default_headers, **headers})

    def start_crawl(self):
        pass


    @staticmethod
    def data_adapter(mapper, raw_data, meta=False):
        mapped_data = { key: raw_data[value] for key, value in mapper }
        if meta:
            mapped_data['meta'] = raw_data
        return mapped_data
