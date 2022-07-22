def product_scraper(product_url: str, need_check: bool, serial_number: int) -> None:
    try:
        driver.switch_to.window(driver.window_handles[serial_number % 2])
        driver.get(product_url)
        time.sleep(1.2)

        soup = BeautifulSoup(markup=driver.page_source, features='html.parser')  # make soup with full markup
        script_tags = soup.find_all(name='script')  # find all existing script tags

        if not need_check:
            '''
            filter only one script tag where products data included. condition is re.findall(condition=r"(window.__PRELOADED_STATE__ = ))
        
            <script type="text/javascript">window.__PRELOADED_STATE__ = {"entities":{"categories":{"137431":{"id":137431,"name":"Women","parentId":0,"gender":0},"137432":{"id":137432,"name":"Clothing","parentId":137431,"gender":0}
            '''
            tags = list(filter(lambda script_tag: re.findall(condition, script_tag.text.strip()), script_tags))
            json_data_text = ""
            for tag in tags:
                json_data_text = json.loads(re.sub(condition, "", tag.text.strip()).strip()).get("entities")

            '''
            Now we are got our desired data which is look like this.
            {
                "entities":{
                    "categories":{
                        "137431":{"id":137431,"name":"Women","parentId":0,"gender":0},
                        "137432":{"id":137432,"name":"Clothing","parentId":137431,"gender":0},
                        "137446":{"id":137446,"name":"Jackets","parentId":137432,"gender":0},
                        "137450":{"id":137450,"name":"Blazers","parentId":137446,"gender":0}
                    },
                    "brands": {...},
                    "products": {...}
                },
                ...
            }
            '''
            categories_values = json_data_text.get("categories").values()
            brands_values = json_data_text.get("brands").values()
            products_values = json_data_text.get("products").values()

            handle_text = ""
            title = ""
            for value in brands_values:
                handle_text = f'{value["slug"]}'
                title = f'{value["name"]}'

            price_text = ""
            custom_product_type = ""
            body_html = ""
            available_sizes = []
            available_colors = []
            images_url = []
            for value in products_values:
                custom_product_type = value["name"]
                body_html = f'{value["description"]}'

                try:
                    price_text = f'{str(value["price"]["includingTaxes"]).replace(",", "")}'
                except KeyError:
                    price_text = "Out of Stock"

                for size in value["sizes"]:
                    if size["name"] == "OS":
                        pass
                    else:
                        product_size = f'{size["name"]}{size["scaleAbbreviation"]}'
                        available_sizes.append(product_size)

                for color in value["colors"]:
                    if color["tags"][0] != "MainColor":
                        available_colors.append(f'{color["color"]["name"]}')
                    else:
                        pass

                for img_urls in value["images"]:
                    big_key = 0
                    img_link = ""
                    for source_key in img_urls["sources"].keys():
                        if int(source_key) > big_key:
                            img_link = img_urls["sources"][source_key]
                    images_url.append(img_link)

            tags = ""
            for value in categories_values:
                tags = value["name"] if tags == "" else f'{tags}, {value["name"]}'

            sizes = []
            for size in available_sizes:
                for _ in available_colors:
                    sizes.append(size)

            if len(available_colors) != 0 and len(available_sizes) != 0:
                colors = available_colors * len(available_sizes)
            elif len(available_colors) == 0 and len(available_sizes) != 0:
                colors = ['No Color'] * len(available_sizes)
            elif len(available_colors) != 0 and len(available_sizes) == 0:
                colors = available_colors
            else:
                colors = ["No Color"]

            price = [price_text for _ in colors]
            image_position = [str(number) for number in range(1, len(images_url) + 1)]
            variant_image = [images_url[0]]
            json_template = JsonTemplate(
                handle_text=handle_text,
                title=title,
                body_html=body_html,
                custom_product_type=custom_product_type,
                tags=tags,
                product_id=product_url,
                colors=colors,
                sizes=sizes,
                price=price,
                image_src=images_url,
                image_position=image_position,
                variant_image=variant_image
            )

            my_data = json_template.main_dict()

            if not db.contains(query.ID == str(product_url)):
                db.insert(my_data)
                url_db.remove(query.product.product_url == product_url)
            else:
                url_db.remove(query.product.product_url == product_url)
            print("complete")
        elif need_check:
            initial_product_id = product_url.split(sep='-')[-1]
            product_urls = []
            color_selector = driver.find_elements(by=By.ID, value='colorSwatch')

            for option in color_selector:
                option_value = option.find_elements(by=By.TAG_NAME, value='option')
                for value in option_value[1:]:
                    product_id = value.get_attribute(name='value')
                    new_url = product_url.replace(initial_product_id, product_id)
                    product_urls.append(new_url)

            if len(product_urls) == 0:
                product_urls.append(product_url)

            if not special_product_db.contains(query.id == initial_product_id):
                special_product_db.insert({'id': initial_product_id, 'urls': product_urls})
                url_db.remove(query.product.product_url == product_url)
            else:
                url_db.remove(query.product.product_url == product_url)

        else:
            pass
    except Exception as ex:
        print(ex)


if __name__ == '__main__':
    import re
    import json
    import time
    from selenium.webdriver.common.by import By
    from bs4 import BeautifulSoup
    from tinydb import TinyDB, Query
    import undetected_chromedriver as uc
    from base_json_template import JsonTemplate

    '''
    1. create a new database file called as harrods_product_info.json for store product informations
        if this file already exist, then file will not create.

    2. Read URL database file for get all products URLs
    3. create a query object for query database.
    '''
    db = TinyDB("harrods_product_info.json")
    url_db = TinyDB("harrods_product_url.json")
    special_product_db = TinyDB("harrods_special_product_url.json")
    product_info = url_db.all()
    query = Query()

    '''
    Chrome Driver Functionally added here
    '''
    base_url = "https://www.harrods.com"
    chrome_options = uc.ChromeOptions()
    driver = uc.Chrome(
        driver_executable_path="../chrome_driver/linux_64/chromedriver",  # input your driver path
        options=chrome_options
    )
    driver.get(base_url)
    time.sleep(1)
    driver.switch_to.new_window(type_hint='tab')

    condition = re.compile(r"(window.__PRELOADED_STATE__ = )")

    for product_data in product_info:
        product_data_info = product_data["product"]
        try:
            product_scraper(
                product_data_info['product_url'],
                product_data_info['need_check'],
                product_info.index(product_data)
            )
        except Exception as e:
            print(e)
