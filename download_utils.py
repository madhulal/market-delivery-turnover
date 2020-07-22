from io import BytesIO
import urllib.request
from zipfile import ZipFile
import ssl
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def download_file(url, dir, file):
    logger.info('Downloaing {} to {}'.format(url, dir + file))
    ssl._create_default_https_context = ssl._create_unverified_context
    try:
        urllib.request.urlretrieve(url, dir + file)
        return True
    except Exception as e:
        logger.warn('Failed to download {} with exception {}'.format(url, e))


def download_zip_file(url, dir):
    logger.info('Downloaing zip from {url} and extracting to {dir}')
    try:
        with urllib.request.urlopen(url) as zipresp:
            with ZipFile(BytesIO(zipresp.read())) as zfile:
                zfile.extractall(dir)
        return True
    except Exception as e:
        logger.warn('Failed to download {} with exception {}'.format(url, e))


def download_zip_file_mozilla_agent(url, dir):
    logger.info(
        'Downloaing zip using mozilla agent from {url} and extracting to {dir}')
    ssl._create_default_https_context = ssl._create_unverified_context
    page = urllib.request.Request(
        url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(page) as zipresp:
            with ZipFile(BytesIO(zipresp.read())) as zfile:
                zfile.extractall(dir)
        return True
    except Exception as e:
        logger.warn('Failed to download {} with exception {}'.format(url, e))
