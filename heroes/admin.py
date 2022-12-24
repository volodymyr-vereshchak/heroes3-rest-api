from django.contrib import admin

from .models import (
    Resource,
    Town,
    Class,
    SecondarySkill,
    Spell,
    Creature,
    Specialty,
    Hero,
)

admin.site.register(Resource)
admin.site.register(Town)
admin.site.register(Class)
admin.site.register(SecondarySkill)
admin.site.register(Spell)
admin.site.register(Creature)
admin.site.register(Specialty)
admin.site.register(Hero)
