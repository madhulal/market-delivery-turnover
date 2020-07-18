from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile


def downloadzipfile(url, dir):
    print('Downloading zip file' + url)
    with urlopen(url) as zipresp:
        with ZipFile(BytesIO(zipresp.read())) as zfile:
            zfile.extractall(dir)
