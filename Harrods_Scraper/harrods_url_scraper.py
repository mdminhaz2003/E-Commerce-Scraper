import time
import json
from tinydb import TinyDB, Query
import undetected_chromedriver as uc
from bs4 import BeautifulSoup

db = TinyDB("harrods_product_url.json")
query = Query()

base_url = "https://www.harrods.com"
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

        soup = BeautifulSoup(markup=driver.page_source, features='html.parser')
        script_info = soup.find(name="script", attrs={'type': 'application/ld+json'})
        page_data = json.loads(script_info.text.strip())

        '''
        page data giving us a very big dictionary but we need only itemListElement part for get information about it.
        page link : https://www.harrods.com/en-bd/shopping/women-clothing?icid=megamenu_shop_women_clothing_all-clothing
        
        "itemListElement":[
            {
                "@type":"ListItem",
                "position":1,
                "name":"Cotton-Blend Single-Breasted Blazer",
                "url":"/en-bd/shopping/shopping/max-mara-cotton-blend-single-breasted-blazer-17662826"
            },
            ...
        ]
        '''
        for product in page_data.get("itemListElement"):
            '''
            Making product url,
            product_url = base url + itemListElement["url"]
            product_url = https://www.harrods.com/en-bd/shopping/shopping/max-mara-cotton-blend-single-breasted-blazer-17662826
            we got this link. But this link is totally invalid. if we visit this link we won't get our desired output from webpage.
            because in this link have double (/shopping/shopping) part and we need to convert it to single (/shopping) then it will work perfectly.
            So let's make it. :)
            '''
            product_url = f'{base_url}{str(product["url"]).replace("/shopping/shopping/", "/shopping")}'

