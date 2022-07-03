import re
import json
from bs4 import BeautifulSoup
from tinydb import TinyDB, Query
import undetected_chromedriver as uc

'''
1. create a new database file called as harrods_product_info.json for store product informations
    if this file already exist, then file will not create.

2. Read URL database file for get all products URLs
3. create a query object for query database.
'''
db = TinyDB("harrods_product_info.json")
url_db = TinyDB("harrods_product_url.json")
urls = url_db.all()
query = Query()

