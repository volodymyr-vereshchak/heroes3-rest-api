from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from heroes.serializers import (
    ResourceSerializer,
    TownSerializer,
    ClassSerializer,
    SecondarySkillSerializer,
    SpellSerializer,
    CreatureSerializer,
    HeroSerializer,
    HeroListSerializer,
    SpeciltyListSerializer
)
from heroes.models import (
    Resource,
    Town,
    Class,
    SecondarySkill,
    Spell,
    Creature,
    Specialty,
    Hero
)


class ResorceView(ModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer


class TownView(ModelViewSet):
    queryset = Town.objects.all()
    serializer_class = TownSerializer


class ClassView(ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer


class SecondarySkillView(ModelViewSet):
    queryset = SecondarySkill.objects.all()
    serializer_class = SecondarySkillSerializer


class SpellView(ModelViewSet):
    queryset = Spell.objects.all()
    serializer_class = SpellSerializer


class CreatureView(ModelViewSet):
    queryset = Creature.objects.all()
    serializer_class = CreatureSerializer


class SpecialtyView(ModelViewSet):
    queryset = Specialty.objects.all()
    serializer_class = SpeciltyListSerializer


class HeroView(ModelViewSet):
    queryset = Hero.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return HeroListSerializer
        return HeroSerializer