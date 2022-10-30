"""Kullanıcı modeli"""

import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from apps.jobs.models import Jobs

class UserManager(BaseUserManager):
    """Custom user manager"""

    def create_user(self, isim, soyisim, email, rol, password=None):
        """Kullanıcı kaydetme fonksiyonu"""

        if not email:
            raise ValueError("Email adresinizi girin.")

        if not password:
            raise ValueError("Şifrenizi girin.")

        email = self.normalize_email(email)

        user = self.model(isim=isim, soyisim=soyisim, email=email, rol=rol)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, isim, soyisim, email, rol, password=None):
        """Superuser kaydetme"""

        user = self.create_user(isim=isim, soyisim=soyisim, email=email, rol=rol, password=password)

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

    def create_admin(self, isim, soyisim, email, rol, password=None):
        """Admin kaydetme"""

        user = self.create_user(isim=isim, soyisim=soyisim, email=email, rol=rol, password=password)

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = False
        user.save(using=self._db)

        return user

    def create_staff(self, isim, soyisim, email, rol, password=None):
        """Yetkili kaydetme"""

        user = self.create_user(isim=isim, soyisim=soyisim, email=email, rol=rol, password=password)

        user.is_admin = False
        user.is_staff = True
        user.is_superuser = False
        user.save(using=self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model"""

    class UserRoles(models.IntegerChoices):
        """Kullanıcı rolleri"""

        IS_VEREN    = 1, _("İşveren")
        IS_ARAYAN   = 2, _("İş Arayan")

    id                  = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True, verbose_name="Kullanıcı ID")
    isim                = models.CharField(max_length=128, verbose_name=_("İsim"), blank=True, null=True)
    soyisim             = models.CharField(max_length=128, verbose_name=_("Soyisim"), blank=True, null=True)
    email               = models.EmailField(max_length=320, verbose_name=_("Email"), unique=True)
    password            = models.CharField(max_length=128, verbose_name=_("Şifre"))
    rol                 = models.IntegerField(choices=UserRoles.choices, verbose_name=_("Kullanıcı Rolü"), default=UserRoles.IS_ARAYAN)
    kaydedilen_ilanlar  = models.ManyToManyField(Jobs, related_name="+", verbose_name="Kaydedilen İlanlar", blank=True)
    basvurulan_ilanlar  = models.ManyToManyField(Jobs, related_name="+", verbose_name="Başvurulan İlanlar", blank=True)
    uyelik_tarihi       = models.DateTimeField(auto_now_add=True ,verbose_name="Üyelik Tarihi")
    son_oturum          = models.DateTimeField(auto_now=True, verbose_name="Son Oturum")
    is_admin            = models.BooleanField(default=False, verbose_name="Yönetici")
    is_active           = models.BooleanField(default=True, verbose_name="Aktif Hesap")
    is_staff            = models.BooleanField(default=False, verbose_name="Personel")
    is_superuser        = models.BooleanField(default=False, verbose_name="Genel Yönetici")

    EMAIL_FIELD         = "email"
    USERNAME_FIELD      = "email"

    REQUIRED_FIELDS = ["isim","soyisim"]

    objects = UserManager()

    def __str__(self):
        return str(self.isim)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    class Meta:
        verbose_name = "Kullanıcı"
        verbose_name_plural = "Kullanıcılar"
