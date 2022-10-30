"""İş ilanı formları"""

from dataclasses import field
from django import forms
from django.contrib import messages
from apps.users.models import User
from apps.jobs.models import Jobs

class CreateJobForm(forms.ModelForm):
    """İş ilanı kayıt formu"""

    class Meta:
        model = Jobs
        fields = [
            "baslik",
            "detaylar",
            "pozisyon",
            "deneyim",
            "ilan_turu",
            "calisma_sekli",
            "aday_sayisi",
            "etiketler",
            "sirket",
            ]


class UpdateJobForm(forms.ModelForm):
    """İş ilanı güncelleme formu"""

    class Meta:
        model = Jobs
        fields  = [
            "baslik",
            "detaylar",
            "pozisyon",
            "deneyim",
            "ilan_turu",
            "calisma_sekli",
            "aday_sayisi",
            "etiketler",
            "sirket",
            ]
