import scrapy
from scrapy.loader import ItemLoader
from ..items import SteamItem


class BestSellingSpider(scrapy.Spider):
    name = "best_selling"
    allowed_domains = ["store.steampowered.com"]
    start_urls = ["https://store.steampowered.com/search/?filter=topsellers"]

    def parse(self, response):
        games = response.css("#search_resultsRows a")

        for game in games:
            loader = ItemLoader(item=SteamItem(), selector=game, response=response)
            loader.add_css("game_url", "a::attr(href)")
            loader.add_css("img_url", "img::attr(src)")
            loader.add_css("game_name", ".title::text")
            loader.add_css("release_date", ".search_released::text")
            loader.add_css("platforms", ".search_name div span::attr(class)")
            loader.add_css("rating", ".search_review_summary::attr(data-tooltip-html)")
            loader.add_css("original_price", ".search_discount_block")
            loader.add_css("discounted_price", ".search_discount_block")
            loader.add_css("discount_rate", ".search_discount_block")

            yield loader.load_item()

        next_page_link = response.css(".pagebtn::attr(href)").getall()[-1]
        if next_page_link:
            yield scrapy.Request(url=next_page_link, callback=self.parse)
