# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_djangoitem import DjangoItem

from heroes.models import (
    Town,
    Creature,
    Spell,
    SecondarySkill,
    Class
)


class TownItem(DjangoItem):
    images = scrapy.Field()
    django_model = Town


class CreatureItem(DjangoItem):
    images = scrapy.Field()
    django_model = Creature


class SpellItem(DjangoItem):
    images = scrapy.Field()
    django_model = Spell


class SecondarySkillItem(DjangoItem):
    images = scrapy.Field()
    django_model = SecondarySkill


class HeroClassItem(DjangoItem):
    django_model = Class
