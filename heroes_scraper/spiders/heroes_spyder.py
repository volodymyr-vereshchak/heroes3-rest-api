import scrapy
import re
from urllib.parse import urljoin

from heroes_scraper.items import (
    TownItem,
    CreatureItem,
    SpellItem,
    SecondarySkillItem,
    HeroClassItem,
    ResourceItem,
    HeroItem,
)


BASE_URL = "https://heroes.thelazy.net/"
TOWN_URL = urljoin(BASE_URL, "index.php/Main_Page")
CREATURE_URL = urljoin(BASE_URL, "index.php/List_of_creatures")
SPELL_URL = urljoin(BASE_URL, "index.php/List_of_spells")
SECONDARY_SKILL_URL = urljoin(BASE_URL, "index.php/Secondary_skill")
CLASS_URL = urljoin(BASE_URL, "index.php/Hero_class")
HERO_URL = urljoin(BASE_URL, "index.php/List_of_heroes")
RESOURCE_URL = urljoin(BASE_URL, "index.php/Resource")


class TownScraper(scrapy.Spider):
    name = "h3town"
    start_urls = [TOWN_URL]

    def parse(self, response: scrapy.http.Response, **kwargs) -> scrapy.Request:
        for town in response.css("tbody span a img")[:10]:
            item = TownItem()
            item["name"] = town.css("img::attr(alt)").extract_first()
            item["picture_url"] = [
                urljoin(BASE_URL, town.css("img::attr(src)").extract_first())
            ]
            yield item


class CreatureScraper(scrapy.Spider):
    name = "h3creature"
    start_urls = [CREATURE_URL]

    def parse(self, response: scrapy.http.Response, **kwargs) -> scrapy.Request:
        for creature in response.css("tbody tr")[1:]:
            item = CreatureItem()
            item["picture_url"] = [
                urljoin(
                    BASE_URL,
                    creature.css(
                        "td:first-child > a:first-child > img::attr(src)"
                    ).get(),
                )
            ]
            item["name"] = creature.css(
                "td:nth-child(1) > a:nth-child(2)::attr(title)"
            ).get()
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
            item["gold"] = (
                creature.css("td:nth-child(12)::text").get().replace("\xa0", "")
            )
            yield item


class SpellScraper(scrapy.Spider):
    name = "h3spell"
    start_urls = [SPELL_URL]

    def parse_detail(self, response, **kwargs):
        item = SpellItem()
        item["name"] = response.css(
            "table:nth-child(2) > tbody > tr:nth-child(1) > td > b::text"
        ).get()
        item["level"] = response.css(
            "tbody > tr:nth-child(4) > td:nth-child(2)::text"
        ).get()
        item["magic_school"] = response.css(
            "tbody > tr:nth-child(3) > td:nth-child(2) > a::text"
        ).get()
        item["description_base"] = "".join(
            response.xpath(
                "//table[2]/tbody/tr[8]/td/table/tbody/tr/td//text()"
            ).getall()
        ).strip()
        item["description_advance"] = "".join(
            response.xpath(
                "//table[2]/tbody/tr[10]/td/table/tbody/tr/td//text()"
            ).getall()
        ).strip()
        item["description_expert"] = "".join(
            response.xpath(
                "//table[2]/tbody/tr[12]/td/table/tbody/tr/td//text()"
            ).getall()
        ).strip()
        item["picture_url"] = [
            urljoin(
                BASE_URL,
                response.css(
                    "table:nth-child(2) > tbody > tr:nth-child(2) > td > a > img::attr(src)"
                ).get(),
            )
        ]
        yield item

    def parse(self, response, **kwargs):
        for spell_tag in response.css("tbody tr")[1:]:
            spell_url = spell_tag.css(
                "td:nth-child(1) > a:nth-child(2)::attr(href)"
            ).get()
            yield scrapy.Request(
                url=urljoin(BASE_URL, spell_url), callback=self.parse_detail
            )


class SecondarySkillScraper(scrapy.Spider):
    name = "h3SecondarySkill"
    start_urls = [SECONDARY_SKILL_URL]

    def parse_skill_detail(self, response):
        item_list = []
        item = SecondarySkillItem()
        item["name"] = response.css("tbody > tr:nth-child(1) > td > b::text").get()
        item["level"] = 0
        item["description"] = (
            response.css("tbody > tr:nth-child(2) > td:nth-child(2)::text")
            .get()
            .strip()
        )
        item["picture_url"] = [
            urljoin(
                BASE_URL,
                response.css(
                    "tbody > tr:nth-child(2) > td:nth-child(1) > a > img::attr(src)"
                ).get(),
            )
        ]
        item_list.append(item)

        item = SecondarySkillItem()
        item["name"] = response.css("tbody > tr:nth-child(1) > td > b::text").get()
        item["level"] = 1
        item["description"] = (
            response.css("tbody > tr:nth-child(3) > td:nth-child(2)::text")
            .get()
            .strip()
        )
        item["picture_url"] = [
            urljoin(
                BASE_URL,
                response.css(
                    "tbody > tr:nth-child(3) > td:nth-child(1) > a > img::attr(src)"
                ).get(),
            )
        ]
        item_list.append(item)

        item = SecondarySkillItem()
        item["name"] = response.css("tbody > tr:nth-child(1) > td > b::text").get()
        item["level"] = 2
        item["description"] = (
            response.css("tbody > tr:nth-child(4) > td:nth-child(2)::text")
            .get()
            .strip()
        )
        item["picture_url"] = [
            urljoin(
                BASE_URL,
                response.css(
                    "tbody > tr:nth-child(4) > td:nth-child(1) > a > img::attr(src)"
                ).get(),
            )
        ]
        item_list.append(item)

        for item in item_list:
            yield item

    def parse(self, response, **kwargs):
        for skill in response.css("tbody tr")[1:]:
            yield scrapy.Request(
                urljoin(BASE_URL, skill.css("td > a::attr(href)").get()),
                self.parse_skill_detail,
            )


class ClassScraper(scrapy.Spider):
    name = "h3class"
    start_urls = [CLASS_URL]

    def parse(self, response, **kwargs):
        for hero_class in response.css("table:nth-child(6) tbody tr"):
            item = HeroClassItem()
            item["name"] = hero_class.css("td:nth-child(1) > a::attr(title)").get()
            item["attack"] = hero_class.css("td:nth-child(3)::text").get()
            item["defense"] = hero_class.css("td:nth-child(4)::text").get()
            item["power"] = hero_class.css("td:nth-child(5)::text").get()
            item["knowledge"] = hero_class.css("td:nth-child(6)::text").get()
            yield item


class ResourceScraper(scrapy.Spider):
    name = "h3resource"
    start_urls = [RESOURCE_URL]

    def parse(self, response, **kwargs):
        resources = response.css(".toclevel-1 .toctext::text").getall()
        resources_img = response.css("[alt*=Resource]::attr(src)").getall()
        for idx in range(len(resources)):
            item = ResourceItem()
            item["name"] = resources[idx]
            item["picture_url"] = [urljoin(BASE_URL, resources_img[idx])]
            yield item


class HeroScraper(scrapy.Spider):
    name = "h3hero"
    start_urls = [HERO_URL]

    def parse(self, response, **kwargs):
        heroes = response.css("tbody tr")
        for hero_url in heroes[1:]:
            item = HeroItem()
            item["name"] = hero_url.css(
                "td:nth-child(1) > a:nth-child(2)::attr(title)"
            ).get()
            item["hero_class"] = hero_url.css("td:nth-child(2) > a::attr(title)").get()
            item["specialty"] = hero_url.css("td:nth-child(4) > a::attr(title)").get()
            item["secondary_skill_first"] = hero_url.css(
                "td:nth-child(6) > a::attr(title)"
            ).get()
            item["secondary_skill_second"] = hero_url.css(
                "td:nth-child(8) > a::attr(title)"
            ).get()
            item["spell"] = hero_url.css(
                "td:nth-child(10) > a:nth-child(2)::text"
            ).get()
            item["picture_url"] = [
                urljoin(
                    BASE_URL,
                    hero_url.css(
                        "td:nth-child(1) > a:nth-child(1) > img::attr(src)"
                    ).get(),
                )
            ]
            yield item
