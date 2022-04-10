import json
from re import sub
from urllib.parse import urljoin
from copy import deepcopy

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

    def _repr_html_(self):
        session = deepcopy(self._session)
        session.params.pop("f")

        text = session.get(self.url).text
        disabled = "Services Directory has been disabled"
        if disabled in text:
            return f"""
            <b>{disabled}</b>\n
            <pre>{json.dumps(self.meta, indent=2)}</pre>
            """
        text = sub(
            r' href="([^"]+)"',
            lambda m: ' href="' + urljoin(self.url, m.group(1)) + '"', text
        )
        return text
