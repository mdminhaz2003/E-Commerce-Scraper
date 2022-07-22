def product_scraper(urls: list, product_id: str) -> None:
    handle_text = ""
    title = ""
    custom_product_type = ""
    price_text = ""
    body_html = ""
    available_sizes = []
    available_colors = []
    images_url = []
    tags = ""
    sizes = []
    variant_image = []

    for url in urls:
        try:
            driver.switch_to.window(driver.window_handles[urls.index(url) % 2])
            driver.get(url)
            time.sleep(1.2)

            soup = BeautifulSoup(markup=driver.page_source, features='html.parser')
            script_tags = soup.find_all(name='script')

            sc_tags = list(filter(lambda script_tag: re.findall(condition, script_tag.text.strip()), script_tags))
            json_data_text = ""
            for sc_tag in sc_tags:
                json_data_text = json.loads(re.sub(condition, "", sc_tag.text.strip()).strip()).get("entities")

            categories_values = json_data_text.get("categories").values()
            brands_values = json_data_text.get("brands").values()
            products_values = json_data_text.get("products").values()

            if urls.index(url) == 0:
                for value in brands_values:
                    handle_text = f'{value["slug"]}'
                    title = f'{value["name"]}'

                for value in categories_values:
                    tags = value["name"] if tags == "" else f'{tags}, {value["name"]}'

                for value in products_values:
                    custom_product_type = f'{value["name"]}'
                    body_html = f'{value["description"]}'

                    try:
                        price_text = f'{str(value["price"]["includingTaxes"]).replace(",", "")}'
                    except KeyError:
                        price_text = "Out of Stock"
            else:
                pass

            for value in products_values:
                for size in value["sizes"]:
                    if size["name"] == "OS":
                        pass
                    else:
                        product_size = f'{size["name"]} {size["scaleAbbreviation"]}'
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

                    if value["images"].index(img_urls) == 0:
                        variant_image.append(img_link)
                    else:
                        pass
            print(f"Checked {url}")
        except Exception as ex:
            print(ex)

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
    json_template = JsonTemplate(
        handle_text=handle_text,
        title=title,
        body_html=body_html,
        custom_product_type=custom_product_type,
        tags=tags,
        product_id=urls[0],
        colors=colors,
        sizes=sizes,
        price=price,
        image_src=images_url,
        image_position=image_position,
        variant_image=variant_image
    )

    my_data = json_template.main_dict()

    if not db.contains(query.ID == str(urls[0])):
        db.insert(my_data)
        special_product_db.remove(query.id == product_id)
    else:
        special_product_db.remove(query.id == product_id)
    print("complete")


if __name__ == '__main__':
    import re
    import json
    import time
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
    special_product_db = TinyDB("harrods_special_product_url.json")
    product_info = special_product_db.all()
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

    for product_urls in product_info:
        url_list = product_urls["urls"]
        try:
            product_scraper(
                urls=url_list,
                product_id=product_urls['id']
            )
        except Exception as e:
            print(e)
