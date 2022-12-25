import os
import uuid

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.text import slugify


def image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)

    filename = f"{slugify(instance.name)}-{uuid.uuid4()}{extension}"
    return os.path.join(f"img/{type(instance).__name__}/", filename)


class Resource(models.Model):
    name = models.CharField(max_length=16, unique=True)
    picture_url = models.ImageField(upload_to=image_file_path, null=True)

    def __str__(self) -> str:
        return f"{self.name}"


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
        return f"{self.name} Attack: {self.attack} Defense: {self.defense} Power: {self.power} Knowledge: {self.knowledge}"


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

    def __str__(self) -> str:
        return f"{self.name} level: {self.level}"


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

    def __str__(self) -> str:
        return f"{self.name}"


class Creature(models.Model):
    name = models.CharField(max_length=64, unique=True)
    town = models.ForeignKey(Town, on_delete=models.CASCADE, null=True)
    level = models.PositiveIntegerField()
    upgrade = models.BooleanField()
    attack = models.PositiveIntegerField()
    defense = models.PositiveIntegerField()
    min_damage = models.PositiveIntegerField()
    max_damage = models.PositiveIntegerField()
    hp = models.PositiveIntegerField()
    speed = models.PositiveIntegerField()
    growth = models.PositiveIntegerField()
    ai_value = models.PositiveIntegerField()
    gold = models.PositiveSmallIntegerField()
    picture_url = models.ImageField(upload_to=image_file_path, null=True)

    def __str__(self) -> str:
        return f"{self.name}"


class Specialty(models.Model):
    creature = models.ForeignKey(
        Creature, on_delete=models.CASCADE, null=True, blank=True
    )
    resource = models.ForeignKey(
        Resource, on_delete=models.CASCADE, null=True, blank=True
    )
    spell = models.ForeignKey(Spell, on_delete=models.CASCADE, null=True, blank=True)
    secondary_skill = models.ForeignKey(
        SecondarySkill, on_delete=models.CASCADE, null=True, blank=True
    )

    @property
    def name(self) -> str:
        if self.creature:
            return f"{self.creature.name}"
        if self.resource:
            return f"{self.resource.name}"
        if self.spell:
            return f"{self.spell.name}"
        if self.secondary_skill:
            return f"{self.secondary_skill.name}"

    def __str__(self) -> str:
        return f"{self.name}"


class Hero(models.Model):
    name = models.CharField(max_length=16, unique=True)
    hero_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE)
    secondary_skill_first = models.ForeignKey(
        SecondarySkill, related_name="first_skill", on_delete=models.CASCADE
    )
    secondary_skill_second = models.ForeignKey(
        SecondarySkill, related_name="second_skill", on_delete=models.CASCADE, null=True
    )
    spell = models.ForeignKey(Spell, on_delete=models.CASCADE, null=True)
    picture_url = models.ImageField(upload_to=image_file_path, null=True)

    def __str__(self) -> str:
        return f"{self.hero_class} {self.name}"

    @staticmethod
    def validate_skill(
        hero_class: int,
        specialty: Specialty,
        secondary_skill_first: int,
        secondary_skill_second: int,
    ):
        necromancy = SecondarySkill.objects.filter(name="Necromancy")
        heroes_necr = Class.objects.filter(name__in=("Death Knight", "Necromancer"))
        if (
            Specialty.objects.get(id=specialty.id).secondary_skill in necromancy
            or secondary_skill_first in necromancy
            or secondary_skill_second in necromancy
            and hero_class not in heroes_necr
        ):
            raise ValidationError(
                "Only Death Knight and Necromancer can have Necromancy!"
            )

    def clean(self) -> None:
        return self.validate_skill(
            self.hero_class,
            self.specialty,
            self.secondary_skill_first,
            self.secondary_skill_second,
        )
