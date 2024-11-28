from setuptools import setup


DESCRIPTION = "Unofficial API Wrapper for the Wayback Machine"
NAME = "waybacktools"
AUTHOR = "radian462"
AUTHOR_EMAIL = "no-number-email@proton.me"
URL = "https://github.com/radian462/waybacktools"
LICENSE = "MIT License"
KEYWORDS = "waybacktools,wayback,waybackmachine"
DOWNLOAD_URL = "https://github.com/radian462/waybacktools"
VERSION = "0.1.2"
PYTHON_REQUIRES = ">=3.8"
INSTALL_REQUIRES = [
    'beautifulsoup4',
    'playwright',
    'requests',
]
PACKAGES = ["waybacktools"]
CLASSIFIERS = [
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3 :: Only",
]

with open("README-EN.md", encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()

setup(
    name=NAME,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    maintainer=AUTHOR,
    maintainer_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    license=LICENSE,
    keywords=KEYWORDS,
    url=URL,
    version=VERSION,
    download_url=DOWNLOAD_URL,
    python_requires=PYTHON_REQUIRES,
    install_requires=INSTALL_REQUIRES,
    packages=PACKAGES,
    classifiers=CLASSIFIERS,
)
