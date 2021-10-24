from requests import Session
import geopandas as gpd


class Base(object):
    current_version: float = None
    supported_types = ['MapServer', 'FeatureServer']

    def __init__(self, url, **kwargs):
        super(Base, self).__init__()
        self.url = url
        self.session = kwargs.get('session') or Session()
        self.meta = self.session.get(self.url, params=dict(f='json')).json()
        self.meta['url'] = self.url
        # self.meta = gpd.GeoDataFrame.from_dict(self.meta)

        self.current_version = self.meta['currentVersion']
