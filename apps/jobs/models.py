"""İş ilanı modeli"""

import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from taggit.managers import TaggableManager
from taggit.models import GenericUUIDTaggedItemBase, TaggedItemBase

User = settings.AUTH_USER_MODEL

class UUIDTaggedItem(GenericUUIDTaggedItemBase, TaggedItemBase):
    """Taggit framework UUID versiyon"""
    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

class Jobs(models.Model):
    """İş ilanları"""

    class Deneyim(models.IntegerChoices):
        """Deneyim düzeyi seçenekleri"""

        STAJYER     = 0, _("Stajyer")
        BASLANGIC   = 1, _("Başlangıç Seviye")
        UZMAN       = 2, _("Uzman")
        UST_DUZEY   = 3, _("Üst Düzey")
        YONETICI    = 4, _("Yönetici")
        HEPSI       = 5, _("Hepsi")

    class CalismaSekli(models.IntegerChoices):
        """Çalışma şekli seçenekleri"""

        IS_YERINDE  = 0, _("İş Yerinde")
        UZAKTAN     = 1, _("Uzaktan")
        HIBRIT      = 2, _("Hibrit")

    class IlanTuru(models.IntegerChoices):
        """İlan türü seçenekleri"""

        FREELANCE       = 0, _("Freelance")
        YARI_ZAMANLI    = 1, _("Yarı Zamanlı")
        TAM_ZAMANLI     = 2, _("Tam Zamanlı")

    id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True, verbose_name=_("İlan ID"))
    baslik          = models.CharField(max_length=256, verbose_name=_("İlan Başlığı"))
    detaylar        = models.TextField(verbose_name=_("İlan Detayları"))
    pozisyon        = models.CharField(max_length=256, verbose_name=_("Pozisyon"))
    deneyim         = models.IntegerField(choices=Deneyim.choices, verbose_name=_("Deneyim Düzeyi"), default=Deneyim.HEPSI)
    ilan_turu       = models.IntegerField(choices=IlanTuru.choices, verbose_name=_("İlan Türü"), default=IlanTuru.TAM_ZAMANLI)
    calisma_sekli   = models.IntegerField(choices=CalismaSekli.choices, verbose_name=_("Çalışma Şekli"), default=CalismaSekli.IS_YERINDE)
    aday_sayisi     = models.IntegerField(verbose_name=_("Alınacak aday sayısı"))
    etiketler       = TaggableManager(through=UUIDTaggedItem)
    adaylar         = models.ManyToManyField(User, related_name="+", verbose_name=_("Başvuran Kişiler"), blank=True)
    sirket          = models.CharField(max_length=256, verbose_name=_("Şirket Adı"))
    ilan_sahibi     = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("İlan Sahibi"))
    ilan_tarihi     = models.DateTimeField(auto_now_add=True, verbose_name=_("İlan Tarihi"))
    guncelleme      = models.DateTimeField(auto_now=True, verbose_name=_("Güncelleme Tarihi"))

    def __str__(self):
        return str(self.baslik)

    class Meta:
        verbose_name = _("İş İlanı")
        verbose_name_plural = _("İş İlanları")
