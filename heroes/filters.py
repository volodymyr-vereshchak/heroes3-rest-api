import django_filters

from .models import Specialty


class SpecialtyFilter(django_filters.FilterSet):
    class Meta:
        model = Specialty
        fields = {
            "creature__name": ["icontains"],
            "resource__name": ["icontains"],
            "spell__name": ["icontains"],
            "secondary_skill__name": ["icontains"],
        }
