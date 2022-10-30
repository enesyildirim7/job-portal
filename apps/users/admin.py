"""Kullanıcı admin sayfası"""

from dataclasses import field
from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from apps.users.models import User
from apps.jobs.models import Jobs

class UserCreationForm(forms.ModelForm):
    isim        = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'class':'form-elements', 'placeholder':'İsim'}), label="İsim")
    soyisim     = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'class':'form-elements', 'placeholder':'Soyisim'}), label="Soyisim")
    email       = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-elements', 'placeholder':'Email'}), label="Email")
    password    = forms.CharField(max_length=64, widget=forms.PasswordInput(attrs={'class':'form-elements', 'placeholder':'Şifre'}), label="Şifre")
    passcheck   = forms.CharField(max_length=64, widget=forms.PasswordInput(attrs={'class':'form-elements', 'placeholder':'Şifre Tekrar'}), label="Şifre Tekrar")
    rol         = forms.ChoiceField(choices=User.UserRoles.choices)

    class Meta:
        model = User
        fields = ("isim", "soyisim", "email", "password", "passcheck", "rol")

    def clean_password2(self):
        """Şifre kontrolü"""

        password = self.cleaned_data.get("password")
        passcheck = self.cleaned_data.get("passcheck")

        if (password and passcheck) and (password != passcheck):
            raise ValidationError("Parolalar eşleşmiyor. Doğru yazdığından emin ol.")

        return passcheck
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get("password"))
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ("isim", "soyisim", "email", "rol", "kaydedilen_ilanlar", "basvurulan_ilanlar") 


class CustomUserAdmin(UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ("isim", "soyisim", "email", "rol")
    list_editable = ["rol"]
    list_filter = ("rol",)

    fieldsets = (
        (None, {"fields": ("isim","soyisim","email","password","basvurulan_ilanlar","kaydedilen_ilanlar")}),
        ("Bilgiler", {"fields": ("rol",)})

    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("isim","soyisim","email","password","passcheck","rol")
        })
    )

    search_fieldsets = ("rol")
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(User, CustomUserAdmin)
