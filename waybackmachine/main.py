from datetime import datetime
from logging import getLogger, StreamHandler, Formatter, DEBUG
from pathlib import Path
import re
from urllib.parse import urlparse

import requests
from playwright.sync_api import sync_playwright

from .exceptions import *


class waybackmachine:
    def __init__(
        self,
        max_tries: int = 5,
        user_agent: str = "",
        proxies: dict = {},
        debug: bool = False,
    ) -> None:
        self.user_agent = user_agent
        self.proxies = proxies
        self.max_tries = max_tries

        self.logger = getLogger("Wayback")
        if debug == True:
            self.logger.setLevel(DEBUG)
        handler = StreamHandler()
        formatter = Formatter("[%(levelname)s] %(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def save(self, url: str, max_tries: int = None) -> str:
        if max_tries is None:
            max_tries = self.max_tries

        for i in range(max_tries):
            try:
                self.logger.debug("Start saving website")
                r = requests.get(
                    "https://web.archive.org/save/" + url, proxies=self.proxies
                )

                if r.status_code == 429:
                    raise TooManyRequestsError(
                        "Your IP has been blocked."
                        "Save Page Now has a limit of 15 requests per minute."
                        "Please try again in 5 minutes."
                    )

                self.logger.debug("Finish saving website")
                return r.url
            except Exception as e:
                self.logger.debug(f"Attempt {i + 1} failed: {e}")
                if i + 1 == max_tries:
                    raise RetryLimitExceededError("The retry limit has been reached.")

    def get(
        self, url: str, timestamp: datetime | str = "latest", max_tries: int = None
    ) -> tuple:
        if max_tries is None:
            max_tries = self.max_tries

        if timestamp not in ["latest", "oldest"] and not isinstance(
            timestamp, datetime
        ):
            raise ValueError(
                "timestamp should be 'latest', 'oldest', or a datetime object"
            )

        for i in range(max_tries):
            try:
                timestamp = (
                    datetime.now()
                    if timestamp == "latest"
                    else (
                        datetime(2001, 10, 24, 0, 0, 0)
                        if timestamp == "oldest"
                        else timestamp
                    )
                )
                timestamp_str = timestamp.strftime("%Y%m%d%H%M%S")

                params = {
                    "url": url,
                    "timestamp": timestamp_str,
                }

                r = requests.get(
                    "https://archive.org/wayback/available",
                    params=params,
                    proxies=self.proxies,
                )

                archive = r.json()["archived_snapshots"].get("closest")
                if archive:
                    archive_url, archive_timestamp = (
                        archive["url"],
                        archive["timestamp"],
                    )
                    archive_timestamp = datetime.strptime(
                        archive_timestamp, "%Y%m%d%H%M%S"
                    )
                    return (archive_url, archive_timestamp)
                else:
                    return ()
            except Exception as e:
                self.logger.debug(f"Attempt {i + 1} failed: {e}")
                if i + 1 == max_tries:
                    raise RetryLimitExceededError("The retry limit has been reached.")

    def download(
        self,
        url: str,
        path: str | None = None,
        ext: str = "mhtml",
        max_tries: int = None,
    ) -> str:
        if max_tries is None:
            max_tries = self.max_tries

        if ext not in ["mhtml", "pdf"]:
            raise ValueError("ext should be 'mhtml' or 'pdf'")

        for i in range(max_tries):
            try:
                self.logger.debug(f"url:{url}")

                if "web.archive.org/web/" not in url:
                    archive_data = self.get(url, max_tries=1)
                    if archive_data:
                        archive_url = archive_data[0]
                        self.logger.debug(f"Archive Found")
                    else:
                        raise NotFoundError("Archive Not Found")
                else:
                    archive_url = url

                playwright_proxy = {}
                if self.proxies:
                    scheme = urlparse(archive_url).scheme
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
                    self.logger.debug(f"Access to {archive_url}")
                    page.goto(archive_url, wait_until="domcontentloaded")

                    if path is None:
                        timestamp = re.search(
                            r"web\.archive\.org/web/(\d+)/", archive_url
                        ).group(1)
                        path = f"{page.title()} - {timestamp}.{ext}"

                    if not path.endswith(ext):
                        path += f".{ext}"

                    if ext == "mhtml":
                        client = page.context.new_cdp_session(page)
                        mhtml = client.send("Page.captureSnapshot")["data"]
                        with open(
                            path, mode="w", encoding="UTF-8", newline="\n"
                        ) as file:
                            file.write(mhtml)
                    elif ext == "pdf":
                        page.pdf(path=path)

                    browser.close()
                    self.logger.debug(f"Browser close")

                    absolute_path = Path(path).resolve()
                return absolute_path

            except Exception as e:
                self.logger.debug(f"Attempt {i + 1} failed: {e}")
                if i + 1 == max_tries:
                    raise RetryLimitExceededError("The retry limit has been reached.")