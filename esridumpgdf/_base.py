import json

from pandas import Series
from requests import Session


class Base(object):
    _supported_services = ["MapServer", "FeatureServer"]
    _supported_types = ["Feature Layer", "Table"]

    def __init__(self, url, session: Session = None):
        super(Base, self).__init__()
        self.url = url
        self._session = session or Session()
        self._session.params.update(dict(f="json"))

        self.meta = self._session.get(self.url).json()
        self.meta["url"] = self.url
        self.current_version = self.meta["currentVersion"]

    def __repr__(self) -> str:
        return Series(self.meta).to_string()

    def _repr_html_(self) -> str:
        return f"<pre>{json.dumps(self.meta, indent=2)}</pre>"
