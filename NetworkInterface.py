import requests


class NetworkInterface():
    # singleton
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        pass

    def get(self, url, param={}):
        response = requests.get(url, param)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            print(error)
            raise RuntimeError(
                'network error: could not connect to ' + url) from exc
        else:
            return response
