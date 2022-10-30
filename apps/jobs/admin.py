from django.contrib import admin
from apps.jobs.models import Jobs


class JobsAdmin(admin.ModelAdmin):

    list_display = (
        "baslik",
        "pozisyon",
        "deneyim",
        "ilan_turu",
        "calisma_sekli",
        "aday_sayisi",
        "sirket",
        "ilan_sahibi",
        "ilan_tarihi",
        "guncelleme"
        )

    fieldsets = (
    (None, {'fields': (
        "baslik",
        "detaylar",
        "pozisyon",
        "deneyim",
        "ilan_turu",
        "calisma_sekli",
        "aday_sayisi",
        "etiketler",
        "sirket",
        "ilan_sahibi",
        )}),
)

admin.site.register(Jobs)
