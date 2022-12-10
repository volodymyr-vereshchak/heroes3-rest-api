from rest_framework import serializers

from heroes.models import (
    Resource,
    Town,
    Skill,
    Class,
    SecondarySkill,
    Spell,
    Creatures,
    Specialty,
    Hero,
)


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ("id", "name")


class TownSerializer(serializers.ModelSerializer):
    class Meta:
        model = Town
        fields = ("id", "name")


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ("id", "attack", "defence", "power", "knowledge")


class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ("id", "name", "skills")


class SecondaeySkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecondarySkill
        fields = ("id", "name", "level", "description")


class SpellSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spell
        fields = ("id", "name", "level", "description")


class CreaturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Creatures
        fields = (
            "id",
            "name",
            "town",
            "level",
            "upgrade",
            "attack",
            "defence",
            "min_damage",
            "max_damage",
            "hp",
            "speed",
            "growth",
            "ai_value",
            "gold",
            "wood",
            "ore",
            "mercury",
            "sulfur",
            "crystal",
            "gems"
        )


class SpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = ("id", "creature", "resource", "spell", "secondary_skill")


class HeroesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hero
        fields = (
            "id", 
            "name", 
            "hero_class", 
            "specialty", 
            "secondary_skill_first",
            "secondary_skill_second",
            "spell"
        )
