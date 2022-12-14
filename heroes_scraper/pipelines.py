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
    CreatureSerializer
)
from heroes.models import (
    Town
)


class HeroesScraperPipeline:
    @sync_to_async
    def process_item(self, item, spider):
        if spider.name == "h3town":
            serializer = TownSerializer(data={"name": item["name"], "picture_url": File(open(os.path.join(IMAGES_STORE, item["images"][0]["path"]), "rb"))})
            if serializer.is_valid():
                serializer.save()
        
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
            if serializer.is_valid():
                serializer.save()
        return item
