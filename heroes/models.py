import os
import uuid

from django.db import models
from django.utils.text import slugify


def image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)

    filename = f"{slugify(instance.name)}-{uuid.uuid4()}{extension}"
    return os.path.join(f"img/{type(instance).__name__}/", filename)


class Resource(models.Model):
    name = models.CharField(max_length=16)
    picture_url = models.ImageField(upload_to=image_file_path, null=True)


class Town(models.Model):
    name = models.CharField(max_length=16, unique=True)
    picture_url = models.ImageField(upload_to=image_file_path, null=True)

    def __str__(self) -> str:
        return f"Town: {self.name}"


class Class(models.Model):
    name = models.CharField(max_length=16, unique=True)
    attack = models.PositiveIntegerField(null=True)
    defense = models.PositiveIntegerField(null=True)
    power = models.PositiveIntegerField(null=True)
    knowledge = models.PositiveIntegerField(null=True)

    def __str__(self) -> str:
        return f"Attack: {self.attack} Defense: {self.defense} Power: {self.power} Knowledge: {self.knowledge}"
    

class SecondarySkill(models.Model):
    class Level(models.IntegerChoices):
        BASE = 0
        ADVANCED = 1
        EXPERT = 2

    name = models.CharField(max_length=32)
    level = models.PositiveIntegerField(choices=Level.choices, null=True)
    description = models.TextField(null=True)
    picture_url = models.ImageField(upload_to=image_file_path, null=True)
    
    class Meta:
        unique_together = ["name", "level"]


class Spell(models.Model):
    class MagicSchool(models.IntegerChoices):
        FIRE = 0
        AIR = 1
        EARTH = 2
        WATER = 3

    name = models.CharField(max_length=64, unique=True)
    level = models.PositiveIntegerField()
    magic_school = models.PositiveIntegerField(choices=MagicSchool.choices, null=True)
    description_base = models.TextField(null=True)
    description_advance = models.TextField(null=True)
    description_expert = models.TextField(null=True)
    picture_url = models.ImageField(upload_to=image_file_path, null=True)


class Creature(models.Model):
    name = models.CharField(max_length=64, unique=True)
    town = models.ForeignKey(Town, on_delete=models.CASCADE, null=True)
    level = models.PositiveIntegerField()
    upgrade = models.BooleanField()
    attack = models.PositiveIntegerField()
    defence = models.PositiveIntegerField()
    min_damage = models.PositiveIntegerField()
    max_damage = models.PositiveIntegerField()
    hp = models.PositiveIntegerField()
    speed = models.PositiveIntegerField()
    growth = models.PositiveIntegerField()
    ai_value = models.PositiveIntegerField()
    gold = models.PositiveSmallIntegerField()
    picture_url = models.ImageField(upload_to=image_file_path, null=True)


class Specialty(models.Model):
    creature = models.ForeignKey(Creature, on_delete=models.CASCADE, unique=True, null=True)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, unique=True, null=True)
    spell = models.ForeignKey(Spell, on_delete=models.CASCADE, unique=True, null=True)
    secondary_skill = models.ForeignKey(SecondarySkill, on_delete=models.CASCADE, unique=True, null=True)


class Hero(models.Model):
    name = models.CharField(max_length=16)
    hero_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE)
    secondary_skill_first = models.ForeignKey(SecondarySkill, related_name="first_skill", on_delete=models.CASCADE)
    secondary_skill_second = models.ForeignKey(SecondarySkill, related_name="second_skill", on_delete=models.CASCADE)
    spell = models.ForeignKey(Spell, on_delete=models.CASCADE)
    picture_url = models.ImageField(upload_to=image_file_path, null=True)
