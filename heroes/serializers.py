from rest_framework import serializers

from heroes.models import (
    Resource,
    Town,
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


class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ("id", "name", "attack", "defense", "power", "knowledge")


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
            "picture_url",
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
            "picture_url",
        )


class SpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = ("id", "creature", "resource", "spell", "secondary_skill", "name")

    def to_representation(self, instance):
        result = super(SpecialtySerializer, self).to_representation(instance)
        return {key: value for key, value in result.items() if value is not None}


class SpecialtyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = ("id", "name")


class SpecialtyDetailSerializer(SpecialtySerializer):
    creature = CreatureSerializer(many=False, read_only=True)
    resource = ResourceSerializer(many=False, read_only=True)
    spell = SpellSerializer(many=False, read_only=True)
    secondary_skill = SecondarySkillSerializer(many=False, read_only=True)


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
            "picture_url",
        )

    def to_representation(self, instance):
        result = super(HeroSerializer, self).to_representation(instance)
        return {key: value for key, value in result.items() if value is not None}

    def validate(self, attrs):
        data = super(HeroSerializer, self).validate(attrs=attrs)
        Hero.validate_skill(
            attrs["hero_class"],
            attrs["specialty"],
            attrs["secondary_skill_first"],
            attrs["secondary_skill_second"],
        )
        return data


class HeroListSerializer(HeroSerializer):
    hero_class = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="name"
    )
    specialty = SpecialtyListSerializer(many=False, read_only=True)
    secondary_skill_first = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="name"
    )
    secondary_skill_second = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="name"
    )
    spell = serializers.SlugRelatedField(many=False, read_only=True, slug_field="name")


class HeroDetailSerializer(HeroSerializer):
    hero_class = ClassSerializer(many=False, read_only=True)
    specialty = SpecialtyDetailSerializer(many=False, read_only=True)
    secondary_skill_first = SecondarySkillSerializer(many=False, read_only=True)
    secondary_skill_second = SecondarySkillSerializer(many=False, read_only=True)
    spell = SpellSerializer(many=False, read_only=True)
