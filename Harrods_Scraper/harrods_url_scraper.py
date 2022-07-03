import json
from tinydb import TinyDB, Query
import undetected_chromedriver as uc
from bs4 import BeautifulSoup

db = TinyDB("harrods_product_url.json")
query = Query()

base_url = "https://www.harrods.com"
chrome_options = uc.ChromeOptions()
driver = uc.Chrome(
    driver_executable_path="../chrome_driver/linux_64/chromedriver",    # input your driver path
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

            '''
            finally, we got our desired product url. Now we need to store this link to a safe place sa that we can use it in future. But we don't want to 
            store duplicate data to our database. That's why, we have to check that this url is already exist or not. 
            if this link is already exist, we have to pass otherwise we have to store in our database called as (harrods_product_url.json)
            '''
            if not db.contains(query.url == product_url):
                db.insert({"url": product_url})
                print(product_url)
            else:
                pass

    except Exception as unknown_exception:
        print(unknown_exception)


'''
For scrap https://www.harrods.com/en-bd/ website's product URL, you have to input a specific types of product page url.
1. Visit this website : https://www.harrods.com/en-bd/
2. Hover on specific types of product categories (Let's say Women)
3. Click on specific types of product (Let's say Tops)
4. Copy the url from URL bar.
   You will get this: https://www.harrods.com/en-bd/shopping/women-clothing-tops?icid=megamenu_shop_women_clothing_tops
   Remember, you URL must be like this. Otherwise it will not work.
5. Paste to page_url variable.
6. Boo oom :)
'''
from_page_number = 1  # From Page
to_page_number = 25  # To Page

page_url = "https://www.harrods.com/en-bd/shopping/women-clothing-tops?icid=megamenu_shop_women_clothing_tops"

for page_number in range(from_page_number, to_page_number + 1):
    main_link = f"{page_url}&pageindex={page_number}"
    try:
        product_url_scraper(page_link=main_link, serial_number=page_number)
    except Exception as exception:
        print(exception)

print("Program Finished...")
