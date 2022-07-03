import time
import json
from tinydb import TinyDB, Query
import undetected_chromedriver as uc
from bs4 import BeautifulSoup

db = TinyDB("harrods_product_url.json")
query = Query()

base_url = "https://www.harrods.com/"
chrome_options = uc.ChromeOptions()
driver = uc.Chrome(
    driver_executable_path="../chrome_driver/chromedriver",
    options=chrome_options
)
driver.get(base_url)
driver.implicitly_wait(time_to_wait=2)
driver.switch_to.new_window(type_hint='tab')

def product_url_scraper(page_link: str, serial_number: int) -> None:
    try:
        driver.switch_to.window(driver.window_handles[serial_number % 2])
        driver.get(page_link)
        driver.implicitly_wait(5)
