from datetime import datetime
import logging
from logging import getLogger, DEBUG
import re
from urllib.parse import urlparse

import requests
from playwright.sync_api import sync_playwright

from exceptions import *


class waybackmachine:
    def __init__(
        self, user_agent: str = "", proxies: dict = {}, debug: bool = False
    ) -> None:
        self.user_agent = user_agent
        self.proxies = proxies

        self.logger = getLogger("Wayback")
        if debug == True:
            self.logger.setLevel(DEBUG)
        handler = logging.StreamHandler()
        formatter = logging.Formatter("[%(levelname)s] %(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def save(self, url: str) -> str:
        self.logger.debug("Start saving website")
        r = requests.get("https://web.archive.org/save/" + url, proxies=self.proxies)

        if r.status_code == 429:
            raise TooManyRequestsError(
                "Your IP has been blocked."
                "Save Page Now has a limit of 15 requests per minute."
                "Please try again in 5 minutes."
            )

        self.logger.debug("Finish saving website")
        return r.url

    def get(self, url: str, timestamp: datetime | str = "latest") -> tuple:
        if timestamp not in ["latest", "oldest"] and not isinstance(
            timestamp, datetime
        ):
            raise ValueError(
                "timestamp should be 'latest', 'oldest', or a datetime object"
            )

        timestamp = (
            datetime.now()
            if timestamp == "latest"
            else datetime(2001, 10, 24, 0, 0, 0) if timestamp == "oldest" else timestamp
        )
        timestamp_str = timestamp.strftime("%Y%m%d%H%M%S")

        params = {
            "url": url,
            "timestamp": timestamp_str,
        }

        r = requests.get(
            "https://archive.org/wayback/available", params=params, proxies=self.proxies
        )

        archive = r.json()["archived_snapshots"].get("closest")
        if archive:
            archive_url, archive_timestamp = archive["url"], archive["timestamp"]
            archive_timestamp = datetime.strptime(archive_timestamp, "%Y%m%d%H%M%S")
            return (archive_url, archive_timestamp)
        else:
            return ()

    def download(self, url: str, path: str | None = None) -> str:
        self.logger.debug(f"url:{url}")
        self.logger.debug(f"path:{path}")

        if not "web.archive.org/web/" in url:
            url = self.get(url)

        if url:
            url = url[0]
        else:
            raise NotFoundError("Archive Not Found")

        playwright_proxy = {}
        if self.proxies:
            scheme = urlparse(url).scheme
            proxy = self.proxies.get(scheme)
            if proxy:
                playwright_proxy = {"server": proxy}
                if "@" in proxy:
                    auth, ip = proxy.split("@")
                    playwright_proxy["server"] = "http://" + ip
                    username, password = auth.split("//")[1].split(":")
                    playwright_proxy["username"] = username
                    playwright_proxy["password"] = password

        with sync_playwright() as playwright:
            launch_options = {"headless": True}
            if playwright_proxy:
                launch_options["proxy"] = playwright_proxy

            browser = playwright.chromium.launch(**launch_options)
            self.logger.debug(f"Browser launch")

            page = browser.new_page()
            self.logger.debug(f"Access to {url}")
            page.goto(url, wait_until="domcontentloaded")

            if path is None:
                timestamp = re.search(r"web\.archive\.org/web/(\d+)/", url).group(1)
                path = f"{page.title()} - {timestamp}.mhtml"

            client = page.context.new_cdp_session(page)
            mhtml = client.send("Page.captureSnapshot")["data"]
            with open(path, mode="w", encoding="UTF-8", newline="\n") as file:
                file.write(mhtml)

            browser.close()
            self.logger.debug(f"Browser close")

        return path


if __name__ == "__main__":
    wayback = waybackmachine(debug=True)
    print(wayback.download("https://github.com/"))
