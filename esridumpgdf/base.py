from requests import Session


class Base(object):
    def __init__(self, url, **kwargs):
        self.url = url
        self.session = kwargs.get('session') or Session()

    @property
    def meta(self) -> dict:
        return self.session.get(self.url, params=dict(f='pjson')).json()
