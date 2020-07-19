from io import BytesIO
import urllib.request
from zipfile import ZipFile
import ssl


def download_file(url, dir, file):
    urllib.request.urlretrieve(url, dir + file)


def download_zip_file(url, dir):
    with urllib.request.urlopen(url) as zipresp:
        with ZipFile(BytesIO(zipresp.read())) as zfile:
            zfile.extractall(dir)


def download_zip_file_mozilla_agent(url, dir):
    ssl._create_default_https_context = ssl._create_unverified_context
    page = urllib.request.Request(
        url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(page) as zipresp:
        with ZipFile(BytesIO(zipresp.read())) as zfile:
            zfile.extractall(dir)
