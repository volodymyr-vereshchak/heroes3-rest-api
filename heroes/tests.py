from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import (
    Resource,
    Town,
    Class,
    SecondarySkill,
    Spell,
    Creature,
    Hero,
    Specialty,
)

from .serializers import ResourceSerializer, HeroListSerializer

HERO_LIST_URL = reverse("heroes:hero-list")
RESOURCE_LIST_URL = reverse("heroes:resource-list")


def create_resource() -> Resource:
    data = {"name": "Gold"}
    return Resource.objects.create(**data)


def create_town() -> Town:
    data = {"name": "Castle"}
    return Town.objects.create(**data)


def create_class() -> Class:
    data = {"name": "Knight", "attack": 2, "defense": 2, "power": 0, "knowledge": 1}
    return Class.objects.create(**data)


def create_secondary_skills() -> list[SecondarySkill]:
    data_first = {"name": "Attack", "level": 0, "description": "test_description"}

    data_second = {"name": "Defense", "level": 0, "description": "test_description"}

    return [
        SecondarySkill.objects.create(**data_first),
        SecondarySkill.objects.create(**data_second),
    ]


def create_spell() -> Spell:
    data = {
        "name": "Arrow",
        "level": 0,
        "magic_school": 1,
    }
    return Spell.objects.create(**data)


def create_creature():
    data = {
        "name": "test_creature",
        "town": create_town(),
        "level": 1,
        "upgrade": False,
        "attack": 1,
        "defense": 1,
        "min_damage": 1,
        "max_damage": 1,
        "hp": 1,
        "speed": 1,
        "growth": 1,
        "ai_value": 1,
        "gold": 1,
    }
    Creature.objects.create(**data)


def create_specialty():
    data = {
        "creature": create_creature(),
    }
    return Specialty.objects.create(**data)


def create_hero():
    skills = create_secondary_skills()
    data = {
        "name": "test_name",
        "hero_class": create_class(),
        "specialty": create_specialty(),
        "secondary_skill_first": skills[0],
        "secondary_skill_second": skills[1],
        "spell": create_spell(),
    }
    return Hero.objects.create(**data)


class UnauthenticatedHeroesApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_anon_user_view_list(self):
        response = self.client.get(HERO_LIST_URL)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_anon_user_post(self):
        response = self.client.post(RESOURCE_LIST_URL, data={"name": "test_name"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedHeroesApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com", "testpass", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_admin_user_post(self):
        response = self.client.post(RESOURCE_LIST_URL, data={"name": "test_name"})
        resource = Resource.objects.get(id=1)
        serializer = ResourceSerializer(resource, many=False)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)

    def test_admin_list(self):
        create_hero()
        response = self.client.get(HERO_LIST_URL)
        heroes = Hero.objects.all()
        serializer = HeroListSerializer(heroes, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)
