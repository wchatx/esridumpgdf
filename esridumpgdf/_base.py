import json
from copy import deepcopy

from pandas import Series
from requests import Session


class Base(object):
    current_version: float = None
    supported_types = ["MapServer", "FeatureServer"]

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
        session = deepcopy(self._session)
        session.params.pop("f")
        text = session.get(self.url).text
        disabled = "Services Directory has been disabled"
        if disabled in text:
            return f"""
            <b>{disabled}</b>\n
            <pre>{json.dumps(self.meta, indent=2)}</pre>
            """
        return text
