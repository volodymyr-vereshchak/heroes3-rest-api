from rest_framework.viewsets import ModelViewSet

from heroes.permissions import IsAdminOrReadOnly

from heroes.serializers import (
    ResourceSerializer,
    TownSerializer,
    ClassSerializer,
    SecondarySkillSerializer,
    SpellSerializer,
    CreatureSerializer,
    SpecialtySerializer,
    SpecialtyListSerializer,
    SpecialtyDetailSerializer,
    HeroSerializer,
    HeroListSerializer,
    HeroDetailSerializer,
)
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

from heroes.filters import SpecialtyFilter


class ResorceView(ModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ["name"]


class TownView(ModelViewSet):
    queryset = Town.objects.all()
    serializer_class = TownSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ["name"]


class ClassView(ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ["name"]


class SecondarySkillView(ModelViewSet):
    queryset = SecondarySkill.objects.all()
    serializer_class = SecondarySkillSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ["name", "level"]


class SpellView(ModelViewSet):
    queryset = Spell.objects.all()
    serializer_class = SpellSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ["name"]


class CreatureView(ModelViewSet):
    queryset = Creature.objects.all()
    serializer_class = CreatureSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ["name"]


class SpecialtyView(ModelViewSet):
    queryset = Specialty.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    filterset_class = SpecialtyFilter

    def get_serializer_class(self):
        if self.action == "list":
            return SpecialtyListSerializer
        if self.action == "retrieve":
            return SpecialtyDetailSerializer
        return SpecialtySerializer


class HeroView(ModelViewSet):
    queryset = Hero.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ["name"]

    def get_serializer_class(self):
        if self.action == "list":
            return HeroListSerializer
        if self.action == "retrieve":
            return HeroDetailSerializer
        return HeroSerializer
