import scrapy
from urllib.parse import urljoin

from heroes_scraper.items import (
    TownItem,
    CreatureItem
)


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
    
    def parse(self, response: scrapy.http.Response, **kwargs) -> scrapy.Request:
        for creature in response.css("tbody tr")[1:]:
            item = CreatureItem()
            item["picture_url"] = [urljoin(
                BASE_URL, creature.css("td:first-child > a:first-child > img::attr(src)").get()
            )]
            item["name"] = creature.css("td:nth-child(1) > a:nth-child(2)::attr(title)").get()
            item["town"] = creature.css("td:nth-child(2) > span > a::attr(title)").get()
            item["level"] = creature.css("[title=Level]::text").get()
            item["upgrade"] = creature.css("[title=Level] sup::text").get()
            item["attack"] = creature.css("[title=Attack]::text").get()
            item["defence"] = creature.css("[title=Defense]::text").get()
            item["min_damage"] = creature.css("[title='Minimum Damage']::text").get()
            item["max_damage"] = creature.css("[title='Maximum Damage']::text").get()
            item["hp"] = creature.css("[title=Health]::text").get()
            item["speed"] = creature.css("[title=Speed]::text").get()
            item["growth"] = creature.css("[title=Growth]::text").get()
            item["ai_value"] = creature.css("[title=AI_Value]::text").get()
            item["gold"] = creature.css("td:nth-child(12)::text").get().replace(u"\xa0", u"")
            yield item