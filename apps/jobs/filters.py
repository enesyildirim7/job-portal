"""Job filtre"""

import django_filters
from django.db.models import Q
from taggit.models import Tag
from apps.jobs.models import Jobs


class JobFilter(django_filters.FilterSet):
    """İş ilanı filtreleme"""

    baslik = django_filters.CharFilter(field_name="baslik",lookup_expr="icontains")
    deneyim = django_filters.MultipleChoiceFilter(choices=Jobs.Deneyim.choices)
    ilan_turu = django_filters.MultipleChoiceFilter(choices=Jobs.IlanTuru.choices)
    calisma_sekli = django_filters.MultipleChoiceFilter(choices=Jobs.CalismaSekli.choices)
    # etiketler = django_filters.ModelMultipleChoiceFilter(choices=Q(Tag.objects.all()))

    class Meta:
        model = Jobs
        fields = [
            "baslik",
            "deneyim",
            "ilan_turu",
            "calisma_sekli",
            # "etiketler"
            ]