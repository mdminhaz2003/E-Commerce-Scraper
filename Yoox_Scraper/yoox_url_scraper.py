import json
from tinydb import TinyDB, Query
import undetected_chromedriver as uc
from bs4 import BeautifulSoup

db = TinyDB("yoox_product_url.json")
query = Query()

base_url = "https://www.yoox.com/us/woman"
chrome_options = uc.ChromeOptions()
driver = uc.Chrome(
    driver_executable_path="../chrome_driver/linux_64/chromedriver",
    options=chrome_options
)
driver.get(base_url)
driver.implicitly_wait(time_to_wait=2)
driver.switch_to.new_window(type_hint='tab')

