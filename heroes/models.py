import os
import uuid

from django.db import models
from django.utils.text import slugify


def image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)

    filename = f"{slugify(instance.name)}-{uuid.uuid4()}{extension}"
    return os.path.join(f"img/{type(instance).__name__}/", filename)


class Level(models.IntegerChoices):
    BASE = 0
    ADVANCED = 1
    EXPERT = 2


class Resource(models.Model):
    name = models.CharField(max_length=16)
    picture_url = models.ImageField(upload_to=image_file_path, null=True)


class Town(models.Model):
    name = models.CharField(max_length=16, unique=True)
    picture_url = models.ImageField(upload_to=image_file_path, null=True)

    def __str__(self) -> str:
        return f"Town: {self.name}"


class Skill(models.Model):
    attack = models.PositiveIntegerField()
    defense = models.PositiveIntegerField()
    power = models.PositiveIntegerField()
    knowledge = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f"Attack: {self.attack} Defense: {self.defense} Power: {self.power} Knowledge: {self.knowledge}"


class Class(models.Model):
    name = models.CharField(max_length=16)
    skills = models.ForeignKey(Skill, on_delete=models.CASCADE)
    

class SecondarySkill(models.Model):
    name = models.CharField(max_length=32)
    level = models.PositiveIntegerField(choices=Level.choices)
    description = models.TextField()
    picture_url = models.ImageField(upload_to=image_file_path, null=True)


class Spell(models.Model):
    name = models.CharField(max_length=64)
    level = models.PositiveIntegerField(choices=Level.choices)
    description = models.TextField()
    picture_url = models.ImageField(upload_to=image_file_path, null=True)


class Creature(models.Model):
    name = models.CharField(max_length=64, unique=True)
    town = models.ForeignKey(Town, on_delete=models.CASCADE)
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
    creature = models.ForeignKey(Creature, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    spell = models.ForeignKey(Spell, on_delete=models.CASCADE)
    secondary_skill = models.ForeignKey(SecondarySkill, on_delete=models.CASCADE)


class Hero(models.Model):
    name = models.CharField(max_length=16)
    hero_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE)
    secondary_skill_first = models.ForeignKey(SecondarySkill, related_name="first_skill", on_delete=models.CASCADE)
    secondary_skill_second = models.ForeignKey(SecondarySkill, related_name="second_skill", on_delete=models.CASCADE)
    spell = models.ForeignKey(Spell, on_delete=models.CASCADE)
    picture_url = models.ImageField(upload_to=image_file_path, null=True)
