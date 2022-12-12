import scrapy
from urllib.parse import urljoin

from heroes_scraper.items import TownItem


BASE_URL = "https://heroes.thelazy.net/index.php/"
TOWN_URL = urljoin(BASE_URL, "Main_Page")
CREATURE_URL = urljoin(BASE_URL, "List_of_creatures")


class TownScraper(scrapy.Spider):
    name = "h3town"
    start_urls = [TOWN_URL]

    def parse(self, response: scrapy.http.Response, **kwargs) -> scrapy.Request:
        for town in response.css("tbody span a img")[:10]:
            item = TownItem()
            item["name"] = town.css("img::attr(alt)").extract_first()            
            item["picture_url"] = [urljoin(BASE_URL, town.css("img::attr(src)").extract_first())]
            yield item


class CreatureScraper(scrapy.Spider):
    name = "h3creature"
    start_urls = [CREATURE_URL]
    
    def parse(self, response, **kwargs):
        return super().parse(response, **kwargs)