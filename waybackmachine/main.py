import requests
import logging
from logging import getLogger, INFO

class waybackmachine():
    def __init__(self):
        self.logger = getLogger("Wayback")
        self.logger.setLevel(INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "[%(levelname)s:%(name)s] %(message)s - %(asctime)s"
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def save(self, url):
        self.logger.info("Start saving website")
        requests.get("https://web.archive.org/save/" + url)
        r = requests.get("https://archive.org/wayback/available?url=" + url)
        archive_url = r.json()["archived_snapshots"]["closest"]["url"]
        self.logger.info("Finish saving website")

        return archive_url

wayback = waybackmachine()
print(wayback.save("https://x.com/TomoMachi/status/1852509638358691990"))
