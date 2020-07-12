from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile
bsebhavzipurl = 'https://www.bseindia.com/download/BhavCopy/Equity/EQ_ISINCODE_100720.zip'
with urlopen(bsebhavzipurl) as zipresp:
    with ZipFile(BytesIO(zipresp.read())) as zfile:
        zfile.extractall('/tmp/bhav')