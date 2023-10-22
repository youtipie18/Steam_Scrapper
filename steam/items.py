# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Selector
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from w3lib.html import remove_tags


def get_discount_price(item):
    selector = Selector(text=item)
    try:
        if int(selector.css("div::attr(data-discount)").get()) > 0:
            return selector.css(".discount_final_price::text").get()
        else:
            return 0
    except TypeError:
        return 0


def get_original_price(item):
    selector = Selector(text=item)
    try:
        if int(selector.css("div::attr(data-discount)").get()) > 0:
            print(selector.css(".discount_original_price"))
            return selector.css(".discount_original_price::text").get()
        else:
            return selector.css(".discount_final_price::text").get()
    except TypeError:
        return 0


def get_discount_rate(item):
    rate = Selector(text=item).css(".search_discount_block::attr(data-discount)").get()
    return int(rate) if rate else 0


def process_price(item):
    if isinstance(item, str):
        return float(item.replace(" ", "").replace(",", ".").replace("€", ""))
    else:
        return item


class SteamItem(scrapy.Item):
    game_url = scrapy.Field(
        output_processor=TakeFirst()
    )
    img_url = scrapy.Field(
        output_processor=TakeFirst()
    )
    game_name = scrapy.Field(
        output_processor=TakeFirst()
    )
    release_date = scrapy.Field(
        output_processor=TakeFirst()
    )
    platforms = scrapy.Field(
        input_processor=MapCompose(lambda item: item.split(" ")[-1].title())
    )
    rating = scrapy.Field(
        input_processor=lambda item: "".join(item).split("<br>")[0] if len(item) else "No info",
        output_processor=TakeFirst()
    )
    original_price = scrapy.Field(
        input_processor=MapCompose(get_original_price, process_price),
        output_processor=TakeFirst()
    )
    discounted_price = scrapy.Field(
        input_processor=MapCompose(get_discount_price, process_price),
        output_processor=TakeFirst()
    )
    discount_rate = scrapy.Field(
        input_processor=MapCompose(get_discount_rate),
        output_processor=TakeFirst()
    )
