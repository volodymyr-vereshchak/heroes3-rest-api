from django.urls import path, include
from rest_framework import routers

from heroes.views import (
    ResorceView,
    TownView,
    ClassView,
    SecondarySkillView,
    SpellView,
    CreatureView,
    SpecialtyView,
    HeroView,
)

router = routers.DefaultRouter()
router.register("resources", ResorceView)
router.register("towns", TownView)
router.register("classes", ClassView)
router.register("secondary-skills", SecondarySkillView)
router.register("spells", SpellView)
router.register("creatures", CreatureView)
router.register("specialtys", SpecialtyView)
router.register("heroes", HeroView)

urlpatterns = [
    path("", include(router.urls)),
]


app_name = "heroes"
