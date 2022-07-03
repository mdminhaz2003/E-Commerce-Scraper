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

'''
Chrome Driver Functionally added here
'''
base_url = "https://www.harrods.com"
chrome_options = uc.ChromeOptions()
driver = uc.Chrome(
    driver_executable_path="../chrome_driver/linux_64/chromedriver",    # input your driver path
    options=chrome_options
)
driver.get(base_url)
driver.implicitly_wait(time_to_wait=2)
driver.switch_to.new_window(type_hint='tab')
