"""User views"""

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import views as auth_views
from apps.users.forms import CustomPasswordResetForm
from apps.users.models import User
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from apps.users.forms import LoginForm, SignupForm, UpdateUserForm, CustomSetPasswordForm

def index(request):
    """Anassayfa"""

    return render(request, "pages/index.html")


def login_view(request):
    """Kullanıcı giriş view"""

    form = LoginForm(request.POST or None)

    context = {"form": form}

    if form.is_valid():
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")

        user = authenticate(email=email, password=password)

        if user is None:
            messages.warning(request, "Şifre hatalı. Tekrar deneyiniz.")
            return render(request, "pages/login.html", context=context)

        login(request, user)
        messages.success(request, f"Başarıyla giriş yapıldı. Hoş geldiniz {request.user.isim}")
        return redirect("user:profile")
    
    return render(request, "pages/login.html", context=context)


def signup_view(request):
    """Kullanıcı kayıt view"""

    form = SignupForm(request.POST or None)

    context = {"form": form}

    if form.is_valid():
        isim = form.cleaned_data.get("isim")
        soyisim = form.cleaned_data.get("soyisim")
        email = form.cleaned_data.get("email")
        rol = form.cleaned_data.get("rol")
        password = form.cleaned_data.get("password")
        passcheck = form.cleaned_data.get("passcheck")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email adresi zaten kayıtlı.")
            return redirect("user:signup")
        
        if password != passcheck:
            messages.error(request, "Şifreler eşleşmiyor.")
            return redirect("user:signup")

        yeni_user = User.objects.create_user(isim=isim, soyisim=soyisim, email=email, rol=rol, password=password)

        login(request,yeni_user)
        messages.success(request, f"Kaydınız başarıyla gerçekleşti. Hoş geldiniz {request.user.isim}")
        return redirect("index")


    return render(request,"pages/signup.html", context=context)


@login_required
def logout_view(request):
    """Kullanıcı logout"""

    logout(request)
    return redirect("index")


@login_required
def user_profile_view(request):
    """Kullanıcı profili"""
    # Kaydedilen ilanlar
    # Başvurulan ilanlar
    # Kullanıcı bilgileri güncelleme

    user = User.objects.get(id=request.user.id)

    if request.method == "POST":
        update_form = UpdateUserForm(request.POST, instance=user)

        if update_form.is_valid():
            update_form.save()
            messages.success(request, "Güncellendi.")
            return redirect("user:profile")

    update_form = UpdateUserForm(instance=user)

    return render(request, "pages/profile.html", {"user_form": update_form})


@login_required
def user_info_view(request,id):
    """Aday bilgileri"""

    user = get_object_or_404(User, id=id)

    return render(request, "pages/aday-profil.html", {"user": user})


@login_required
def user_basvurulan_view(request):
    """Kullanıcının başvurduğu iş ilanları"""

    user = User.objects.prefetch_related("basvurulan_ilanlar").get(id=request.user.id)
    basvurulan = user.basvurulan_ilanlar.all()

    return render(request, "pages/basvurulan.html", {"basvurulan":basvurulan})


@login_required
def user_kaydedilen_view(request):
    """Kullanıcının kaydettiği iş ilanları"""

    user = User.objects.prefetch_related("kaydedilen_ilanlar").get(id=request.user.id)
    kaydedilen = user.kaydedilen_ilanlar.all()

    return render(request, "pages/kaydedilen.html", {"kaydedilen":kaydedilen})



class ChangePasswordView(PasswordChangeView, SuccessMessageMixin):
    """Şifre değiştirme"""

    template_name = "pages/password-change.html"
    success_message = "Şifre değiştirildi."
    success_url = reverse_lazy("user:profile")


def password_reset_view(request):
    """Şifre sıfırlama"""
    if request.method == "POST":
        password_reset_form = CustomPasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password_reset_email.txt"
                    c = {
					"email":user.email,
					"domain":"127.0.0.1:8000",
					"site_name": "Baykar Kariyer",
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					"token": default_token_generator.make_token(user),
					"protocol": "http",
					}
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, "info.enesyildirim@gmail.com" , [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse("Geçersiz başlık.")
                    return redirect ("user:password-reset-done")
    password_reset_form = CustomPasswordResetForm()

    return render(request, template_name="pages/password-reset.html", context={"password_reset_form":password_reset_form})


class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    """Yeni şifre set etme view"""

    form_class = CustomSetPasswordForm
    success_url = reverse_lazy("user:password-reset-complete")


def custom404(request, exception):
    """Özel 404 sayfası"""

    return render(request, "pages/errors/custom404.html", status=404)
