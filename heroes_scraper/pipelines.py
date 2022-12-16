# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os
from asgiref.sync import sync_to_async

from django.core.files import File
from heroes_scraper.settings import IMAGES_STORE
from heroes.serializers import (
    TownSerializer,
    CreatureSerializer,
    SpellSerializer,
    SecondarySkillSerializer
)
from heroes.models import (
    Town
)


class HeroesScraperPipeline:
    @sync_to_async
    def process_item(self, item, spider):
        if spider.name == "h3town":
            serializer = TownSerializer(data={"name": item["name"], "picture_url": File(open(os.path.join(IMAGES_STORE, item["images"][0]["path"]), "rb"))})

        if spider.name == "h3creature":
            try:
                town = Town.objects.get(name=item["town"])
            except Town.DoesNotExist:
                town = None
            serializer = CreatureSerializer(
                data={
                    "name": item["name"],
                    "town": town.id if town else None,
                    "level": int(item["level"]),
                    "upgrade": True if item["upgrade"] else False,
                    "attack": int(item["attack"]),
                    "defence": int(item["defence"]),
                    "min_damage": int(item["min_damage"]),
                    "max_damage": int(item["max_damage"]),
                    "hp": int(item["hp"]),
                    "speed": int(item["speed"]),
                    "growth": int(item["growth"]),
                    "ai_value": int(item["ai_value"]),
                    "gold": int(item["gold"]),
                    "picture_url": File(open(os.path.join(IMAGES_STORE, item["images"][0]["path"]), "rb"))
                }
            )

        if spider.name == "h3spell":
            if "1" in item["level"]:
                level = 1
            if "2" in item["level"]:
                level = 2
            if "3" in item["level"]:
                level = 3
            if "4" in item["level"]:
                level = 4
            if "5" in item["level"]:
                level = 5

            magic_school = item["magic_school"].split()[0]
            if magic_school == "Fire":
                school = 0
            if magic_school == "Air":
                school = 1
            if magic_school == "Earth":
                school = 2
            if magic_school == "Water":
                school = 3

            serializer = SpellSerializer(
                data={
                    "name": item["name"],
                    "level": level,
                    "magic_school": school,
                    "description_base": item["description_base"],
                    "description_advance": item["description_advance"],
                    "description_expert": item["description_expert"],
                    "picture_url": File(open(os.path.join(IMAGES_STORE, item["images"][0]["path"]), "rb"))
                }
            )

        if spider.name == "h3SecondarySkill":
            serializer = SecondarySkillSerializer(
                data={
                    "name": item["name"],
                    "level": item["level"],
                    "description": item["description"],
                    "picture_url": File(open(os.path.join(IMAGES_STORE, item["images"][0]["path"]), "rb")) 
                }
            )

        if serializer.is_valid():
            serializer.save()

        return item
