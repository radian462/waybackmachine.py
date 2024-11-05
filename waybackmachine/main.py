from datetime import datetime
import logging
from logging import getLogger, INFO

import requests

from exceptions import *


class waybackmachine:
    def __init__(self, user_agent: str = "", proxy: dict = {}) -> None:
        self.user_agent = user_agent
        self.proxy = proxy

        self.logger = getLogger("Wayback")
        self.logger.setLevel(INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter("[%(levelname)s] %(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def save(self, url: str) -> str:
        self.logger.info("Start saving website")
        r = requests.get("https://web.archive.org/save/" + url)

        if r.status_code == 429:
            raise TooManyRequestsError(
                "Your IP has been blocked."
                "Save Page Now has a limit of 15 requests per minute."
                "Please try again in 5 minutes."
            )

        self.logger.info("Finish saving website")
        return r.url

    def get(self, url: str, timestamp: datetime = None) -> tuple:
        timestamp = datetime.now() if timestamp is None else timestamp
        timestamp_str = timestamp.strftime("%Y%m%d%H%M%S")
        params = {
            "url": url,
            "timestanp": timestamp_str,
        }
        r = requests.get("https://archive.org/wayback/available", params=params)

        archive = r.json().get('archived_snapshots', {}).get('closest')
        if archive:
            archive_url, archive_timestamp = archive['url'], archive['timestamp']
            return (archive_url, archive_timestamp)
        else:
            return ()

if __name__ == "__main__":
    wayback = waybackmachine()
    