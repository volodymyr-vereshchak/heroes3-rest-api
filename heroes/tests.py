from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

HERO_URL_LIST = reverse("heroes:hero-list")

class UnauthenticatedHeroesApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
    
    def test_anon_user_view_list(self):
        response = self.client.get(HERO_URL_LIST)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
    
    # def test_anon_user_add(self):
    #     response = self.client.post(HERO_URL_LIST, data=)

