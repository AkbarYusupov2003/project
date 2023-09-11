from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

from accounts import views
from accounts.forms import PwdResetForm, PwdResetConfirmForm

app_name = "accounts"

urlpatterns = [
    # Auth
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="accounts:login"), name="logout"),
    path(
        "activate/<slug:uidb64>/<slug:token>/",
        views.AccountActivationView.as_view(),
        name="activate",
    ),
    # Password Reset
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="accounts/password_reset/reset.html",
            email_template_name="accounts/password_reset/email_message.html",
            success_url=reverse_lazy("accounts:password_reset_done"),
            form_class=PwdResetForm,
        ),
        name="password-reset"
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="accounts/password_reset/done.html"
        ),
        name="password_reset_done"
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset/confirm.html",
            success_url=reverse_lazy("accounts:password_reset_complete"),
            form_class=PwdResetConfirmForm,
        ),
        name="password_reset_confirm"
    ),
    path(
        "password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/password_reset/complete.html"
        ),
        name="password_reset_complete"
    ),
    # Edit
    path("settings/", views.SettingsView.as_view(), name="settings"),
    # View
    path("<int:pk>/", views.AccountDetailView.as_view(), name="account-detail"),
]
