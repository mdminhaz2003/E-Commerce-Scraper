def value_adder(max_value: int, data_set: list, value: str) -> None:
    if max_value > len(data_set):
        difference_between = max_value - len(data_set)
        for _ in range(difference_between):
            data_set.append(value)
    else:
        pass


class JsonTemplate:
    def __init__(
            self,
            handle_text: str,
            title: str,
            body_html: str,
            custom_product_type: str,
            tags: str,
            product_id: str,
            colors: list,
            sizes: list,
            price: list,
            image_src: list,
            image_position: list,
            variant_image: list
    ) -> None:
        self.handle_text = f'"{handle_text}"'
        self.title = f'"{title}"'
        self.body_html = f'"{body_html}"'
        self.custom_product_type = f'"{custom_product_type}"'
        self.tags = f'"{tags}"'
        self.product_id = product_id
        self.colors = colors
        self.sizes = sizes
        self.price = price
        self.image_src = image_src
        self.image_position = image_position
        self.variant_image = variant_image
        self.handle = []
        self.variant_inventory_policy = []
        self.variant_fulfilment_service = []
        self.variant_require_shipping = []
        self.variant_taxable = []
        self.variant_weight_unit = []

    def list_equal(self) -> None:
        max_value = max(len(self.colors), len(self.sizes), len(self.image_src))
        if max_value == len(self.colors) == len(self.sizes) == len(self.image_src) == len(self.variant_image):
            value_adder(max_value=max_value, data_set=self.handle, value=self.handle_text)
            value_adder(max_value=max_value, data_set=self.variant_inventory_policy, value="deny")
            value_adder(max_value=max_value, data_set=self.variant_fulfilment_service, value="manual")
            value_adder(max_value=max_value, data_set=self.variant_require_shipping, value="TRUE")
            value_adder(max_value=max_value, data_set=self.variant_taxable, value="TRUE")
            value_adder(max_value=max_value, data_set=self.variant_weight_unit, value="g")
        else:
            value_adder(max_value=max_value, data_set=self.colors, value="")
            value_adder(max_value=max_value, data_set=self.sizes, value="")
            value_adder(max_value=max_value, data_set=self.price, value="")
            value_adder(max_value=max_value, data_set=self.image_src, value="")
            value_adder(max_value=max_value, data_set=self.image_position, value="")
            value_adder(max_value=max_value, data_set=self.variant_image, value="")
            value_adder(max_value=max_value, data_set=self.handle, value=self.handle_text)
            value_adder(max_value=max_value, data_set=self.variant_inventory_policy, value="deny")
            value_adder(max_value=max_value, data_set=self.variant_fulfilment_service, value="manual")
            value_adder(max_value=max_value, data_set=self.variant_require_shipping, value="TRUE")
            value_adder(max_value=max_value, data_set=self.variant_taxable, value="TRUE")
            value_adder(max_value=max_value, data_set=self.variant_weight_unit, value="g")

    def main_dict(self) -> dict:
        self.list_equal()
        data = {
            "Handle": self.handle,
            "Title": self.title,
            "Body (HTML)": self.body_html,
            "Vendor": "Eslam Hosny M.",
            "Standardized Product Type": "",
            "Custom Product Type": self.custom_product_type,
            "Tags": self.tags,
            "Published": "TRUE",
            "ID": self.product_id,
            "Option1 Name": "Color",
            "Option1 Value": self.colors,
            "Option2 Name": "Size",
            "Option2 Value": self.sizes,
            "Option3 Name": "",
            "Option3 Value": "",
            "Variant SKU": "",
            "Variant Grams": "",
            "Variant Inventory Tracker": "",
            "Variant Inventory Qty": "",
            "Variant Inventory Policy": self.variant_inventory_policy,
            "Variant Fulfillment Service": self.variant_fulfilment_service,
            "Variant Price": self.price,
            "Variant Compare At Price": "",
            "Variant Requires Shipping": self.variant_require_shipping,
            "Variant Taxable": self.variant_taxable,
            "Variant Barcode": "",
            "Image Src": self.image_src,
            "Image Position": self.image_position,
            "Image Alt Text": "",
            "Gift Card": "FALSE",
            "SEO Title": "",
            "SEO Description": "",
            "Google Shopping / Google Product Category": "",
            "Google Shopping / Gender": "",
            "Google Shopping / Age Group": "",
            "Google Shopping / MPN": "",
            "Google Shopping / AdWords Grouping": self.custom_product_type,
            "Google Shopping / AdWords Labels": "",
            "Google Shopping / Condition": "",
            "Google Shopping / Custom Product": "FALSE",
            "Google Shopping / Custom Label 0": "",
            "Google Shopping / Custom Label 1": "",
            "Google Shopping / Custom Label 2": "",
            "Google Shopping / Custom Label 3": "",
            "Google Shopping / Custom Label 4": "",
            "Variant Image": self.variant_image,
            "Variant Weight Unit": self.variant_weight_unit,
            "Variant Tax Code": "",
            "Cost per item": "",
            "Status": "active"
        }
        return data

