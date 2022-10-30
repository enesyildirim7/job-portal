from dataclasses import field
from django import forms
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from apps.users.models import User

class LoginForm(forms.Form):
    """Kullanıcı giriş formu"""

    email       = forms.CharField(widget=forms.EmailInput(attrs={"class":"form-elements", "placeholder":"Email"}), label="Email")
    password    = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-elements", "placeholder":"Şifre"}), label="Şifre")

    def clean_email(self):
        """Email kontrol"""

        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email__iexact=email)
        if not qs.exists():
            raise forms.ValidationError("Böyle bir kullanıcı yok.")

        return email


class SignupForm(forms.Form):
    """Kullanıcı kayıt formu"""

    ROL = [
        (1, "İşverenim"),
        (2, "İş arıyorum")
    ]

    isim        = forms.CharField(max_length=128, widget=forms.TextInput(attrs={"class":"form-elements", "placeholder":"İsim"}), label="İsim", required=True)
    soyisim     = forms.CharField(max_length=128, widget=forms.TextInput(attrs={"class":"form-elements", "placeholder":"Soyisim"}), label="Soyisim", required=True)
    email       = forms.EmailField(widget=forms.EmailInput(attrs={"class":"form-elements", "placeholder":"Email"}), label="Email", required=True)
    rol         = forms.ChoiceField(choices=User.UserRoles.choices)
    password    = forms.CharField(max_length=128, widget=forms.PasswordInput(attrs={"class":"form-elements", "placeholder":"Şifre"}), label="Şifre", required=True)
    passcheck   = forms.CharField(max_length=128, widget=forms.PasswordInput(attrs={"class":"form-elements", "placeholder":"Şifre Tekrar"}), label="Şifre Tekrar", required=True)

    class Meta:
        model = User
        fields = ["isim","soyisim","email","password","rol"]

    def clean(self):
        isim        = self.cleaned_data.get("isim")
        soyisim     = self.cleaned_data.get("soyisim")
        email       = self.cleaned_data.get("email")
        rol         = self.cleaned_data.get("rol")
        password    = self.cleaned_data.get("password")
        passcheck   = self.cleaned_data.get("passcheck")

        user_data = {
            "isim": isim,
            "soyisim": soyisim,
            "email": email,
            "rol":rol,
            "password": password,
            "passcheck": passcheck
            }

        return user_data


class UpdateUserForm(forms.ModelForm):
    """Kullanıcı bilgileri güncelleme formu"""

    class Meta:
        model = User
        fields = ["isim", "soyisim", "email"]


class CustomPasswordResetForm(PasswordResetForm):
    """Şifre sıfırlama formu"""

    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={"class":"form-elements","autocomplete": "email"}),
    )


class CustomSetPasswordForm(SetPasswordForm):
    """Yeni şifre set etme"""

    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class":"form-elements","autocomplete": "new-password"}),
        strip=False,
    )
    new_password2 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={"class":"form-elements","autocomplete": "new-password"}),
    )


