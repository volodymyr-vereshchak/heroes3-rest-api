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
    SecondarySkillSerializer,
    ClassSerializer,
    ResourceSerializer,
    HeroSerializer,
)
from heroes.models import (
    Town,
    Class,
    Creature,
    Resource,
    Spell,
    SecondarySkill,
    Specialty,
)


class HeroesScraperPipeline:
    @staticmethod
    def get_skill_level(skill_level: str) -> int:
        if skill_level == "Basic":
            return 0
        if skill_level == "Advanced":
            return 1

    @sync_to_async
    def process_item(self, item, spider):
        if spider.name == "h3town":
            serializer = TownSerializer(
                data={
                    "name": item["name"],
                    "picture_url": File(
                        open(
                            os.path.join(IMAGES_STORE, item["images"][0]["path"]), "rb"
                        )
                    ),
                }
            )

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
                    "defense": int(item["defense"]),
                    "min_damage": int(item["min_damage"]),
                    "max_damage": int(item["max_damage"]),
                    "hp": int(item["hp"]),
                    "speed": int(item["speed"]),
                    "growth": int(item["growth"]),
                    "ai_value": int(item["ai_value"]),
                    "gold": int(item["gold"]),
                    "picture_url": File(
                        open(
                            os.path.join(IMAGES_STORE, item["images"][0]["path"]), "rb"
                        )
                    ),
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

            magic_school = item["magic_school"]
            if magic_school is not None:
                magic_school = magic_school.split()[0]
                if magic_school == "Fire":
                    school = 0
                if magic_school == "Air":
                    school = 1
                if magic_school == "Earth":
                    school = 2
                if magic_school == "Water":
                    school = 3
            else:
                school = None

            serializer = SpellSerializer(
                data={
                    "name": item["name"],
                    "level": level,
                    "magic_school": school,
                    "description_base": item["description_base"],
                    "description_advance": item["description_advance"],
                    "description_expert": item["description_expert"],
                    "picture_url": File(
                        open(
                            os.path.join(IMAGES_STORE, item["images"][0]["path"]), "rb"
                        )
                    ),
                }
            )

        if spider.name == "h3SecondarySkill":
            serializer = SecondarySkillSerializer(
                data={
                    "name": item["name"],
                    "level": item["level"],
                    "description": item["description"],
                    "picture_url": File(
                        open(
                            os.path.join(IMAGES_STORE, item["images"][0]["path"]), "rb"
                        )
                    ),
                }
            )

        if spider.name == "h3class":
            serializer = ClassSerializer(
                data={
                    "name": item["name"],
                    "attack": item["attack"],
                    "defense": item["defense"],
                    "power": item["power"],
                    "knowledge": item["knowledge"],
                }
            )

        if spider.name == "h3resource":
            serializer = ResourceSerializer(
                data={
                    "name": item["name"],
                    "picture_url": File(
                        open(
                            os.path.join(IMAGES_STORE, item["images"][0]["path"]), "rb"
                        )
                    ),
                }
            )

        if spider.name == "h3hero":
            hero_class = Class.objects.get(name=item["hero_class"])
            creature = Creature.objects.filter(name__icontains=item["specialty"][:-1])
            resource = Resource.objects.filter(name=item["specialty"])
            spell = Spell.objects.filter(name=item["specialty"])
            secondary_skill = SecondarySkill.objects.filter(name=item["specialty"])
            if creature:
                specialty = Specialty.objects.get_or_create(creature=creature[0])
            if resource:
                specialty = Specialty.objects.get_or_create(resource=resource[0])
            if spell:
                specialty = Specialty.objects.get_or_create(spell=spell[0])
            if secondary_skill:
                specialty = Specialty.objects.get_or_create(
                    secondary_skill=secondary_skill[0]
                )
            first_skill_level, first_skill = item["secondary_skill_first"].split(" ", 1)
            first_skill_level = self.get_skill_level(first_skill_level)
            secondary_skill_first = SecondarySkill.objects.get(
                name=first_skill, level=first_skill_level
            )
            second_skill_level, second_skill = (
                item["secondary_skill_second"].split(" ", 1)
                if item["secondary_skill_second"]
                else (None, None)
            )
            second_skill_level = self.get_skill_level(second_skill_level)
            secondary_skill_second = (
                SecondarySkill.objects.get(
                    name=second_skill, level=second_skill_level
                ).id
                if second_skill
                else None
            )
            spell_hero = (
                Spell.objects.get(name=item["spell"]).id if item["spell"] else None
            )

            serializer = HeroSerializer(
                data={
                    "name": item["name"],
                    "hero_class": hero_class.id,
                    "specialty": specialty[0].id,
                    "secondary_skill_first": secondary_skill_first.id,
                    "secondary_skill_second": secondary_skill_second,
                    "spell": spell_hero,
                    "picture_url": File(
                        open(
                            os.path.join(IMAGES_STORE, item["images"][0]["path"]), "rb"
                        )
                    ),
                }
            )

        if serializer.is_valid():
            serializer.save()

        return item
