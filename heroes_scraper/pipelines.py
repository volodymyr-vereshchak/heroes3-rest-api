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
            town = Town.objects.get(name=item["name"])            
            serializer = CreatureSerializer(
                data={
                    "name": item["name"],
                    "town": town,
                    "level": int(item["level"]),
                    "upgrade": item["upgrade"],
                    "attack": int(item["attack"]),
                    "defence": int(item["defence"]),
                    
                }
            )
        return item
