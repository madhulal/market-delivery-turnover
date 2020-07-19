from io import BytesIO
import urllib.request
from zipfile import ZipFile
import ssl
import logging

logger = logging.getLogger(__name__)

def download_file(url, dir, file):
    logger.info('Downloaing {} to {}'.format(url, dir+file))
    ssl._create_default_https_context = ssl._create_unverified_context
    urllib.request.urlretrieve(url, dir + file)


def download_zip_file(url, dir):
    logger.info('Downloaing zip from {} and extracting to {}'.format(url, dir))
    with urllib.request.urlopen(url) as zipresp:
        with ZipFile(BytesIO(zipresp.read())) as zfile:
            zfile.extractall(dir)


def download_zip_file_mozilla_agent(url, dir):
    logger.info('Downloaing zip using mozilla agent from {} and extracting to {}'.format(url, dir))
    ssl._create_default_https_context = ssl._create_unverified_context
    page = urllib.request.Request(
        url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(page) as zipresp:
        with ZipFile(BytesIO(zipresp.read())) as zfile:
            zfile.extractall(dir)
