from rest_framework import serializers

from heroes.models import (
    Resource,
    Town,
    Skill,
    Class,
    SecondarySkill,
    Spell,
    Creature,
    Specialty,
    Hero,
)


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ("id", "name", "picture_url")


class TownSerializer(serializers.ModelSerializer):
    class Meta:
        model = Town
        fields = ("id", "name", "picture_url")


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ("id", "attack", "defense", "power", "knowledge")


class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ("id", "name", "skills")


class SecondarySkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecondarySkill
        fields = (
            "id",
            "name",
            "level",
            "description",
            "picture_url",
        )


class SpellSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spell
        fields = (
            "id",
            "name",
            "level",
            "magic_school",
            "description_base",
            "description_advance",
            "description_expert",
            "picture_url"
        )


class CreatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Creature
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
            "picture_url"
        )


class SpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = ("id", "creature", "resource", "spell", "secondary_skill")


class HeroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hero
        fields = (
            "id", 
            "name", 
            "hero_class", 
            "specialty", 
            "secondary_skill_first",
            "secondary_skill_second",
            "spell",
            "picture_url"
        )
