# settings.py
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

LOG_FILE = os.environ.get("LOG_FILE")
DATA_FOLDER = os.environ.get("DATA_FOLDER")
MONGO_URI = os.environ.get("MONGO_URI")
DATE_FORMAT = os.environ.get("DATE_FORMAT")
FUNDAMENTALS_FILE_NAME = os.environ.get("FUNDAMENTALS_FILE_NAME")
