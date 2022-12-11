# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os
from asgiref.sync import sync_to_async

from heroes.serializers import TownSerializer
from heroes_scraper.settings import IMAGES_STORE
from django.core.files import File


class HeroesScraperPipeline:
    @sync_to_async
    def process_item(self, item, spider):
        serializer = TownSerializer(data={"name": item["name"], "picture_url": File(open(os.path.join(IMAGES_STORE, item["images"][0]["path"]), "rb"))})
        if serializer.is_valid():
            serializer.save()
        return item
