import time
import json
from tinydb import TinyDB, Query
import undetected_chromedriver as uc
from bs4 import BeautifulSoup

db = TinyDB("harrods_product_url.json")
query = Query()
