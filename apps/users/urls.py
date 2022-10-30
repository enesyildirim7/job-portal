from django.urls import path
from apps.users import views
from django.contrib.auth import views as auth_views

app_name = "users"

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.user_profile_view, name="profile"),
    path("<uuid:id>/", views.user_info_view, name="info"),
    path("profile/basvurulanlar/", views.user_basvurulan_view, name="basvurulan"),
    path("profile/kaydedilenler/", views.user_kaydedilen_view, name="kaydedilen"),
    path("password-change/", views.ChangePasswordView.as_view(), name="password-change"),
    path("password-reset/", views.password_reset_view, name="password-reset"),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(template_name="pages/password-reset-done.html"), name="password-reset-done"),
    path("password-reset/reset/<uidb64>/<token>/", views.CustomPasswordResetConfirmView.as_view(template_name="pages/password-reset-confirm.html"), name="password-reset-confirm"),
    path("password-reset/reset/done/", auth_views.PasswordResetCompleteView.as_view(template_name="pages/password-reset-complete.html"), name="password-reset-complete")

]