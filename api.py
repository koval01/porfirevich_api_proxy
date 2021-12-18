import logging

import requests
from requests import get


class PorfirevichApi:
    def __init__(self) -> None:
        self.url = "https://porfirevich.ru/api/story"
        self.limit = 20
        self.offset = 0
        self.order = "RAND()"

    @staticmethod
    def check_json(resp_body: requests.get) -> dict or None:
        try:
            body = resp_body.json()["data"]
            if len(body):
                return body
        except Exception as e:
            logging.warning("Check JSON error: %s" % e)
        return None

    def get_json(self) -> list:
        resp = get(url=self.url, params={
            "limit": self.limit, "offset": self.offset,
            "orderBy": self.order
        })
        if resp.status_code >= 200 < 400:
            return self.check_json(resp)
