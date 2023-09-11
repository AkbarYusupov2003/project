from django.contrib.auth import login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View

from accounts import forms
from accounts.tasks import send_activation_email_task
from accounts.tokens import account_activation_token


# Auth
class RegisterView(View):
    template_name = "accounts/register/main.html"
    form_class = forms.RegisterForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {"form": self.form_class})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])
            user.save()
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)
            send_activation_email_task.delay(
                uid, token, user.username, user.email
            )
            return render(
                request, "accounts/register/email_confirm.html"
            )

        return render(request, self.template_name, {"form": form})


class LoginView(View):
    template_name = "accounts/login/main.html"
    form_class = forms.LoginForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {"form": self.form_class})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            user = get_user_model().objects.filter(email=email).first()
            if user:
                if user.check_password(password):
                    login(request, user)
                    return redirect("posts:main")

        return render(
            request, self.template_name, {"form": form, "login_error": True}
        )


class AccountActivationView(View):
    template_name = "accounts/register/activation_invalid.html"

    def get(self, request, uidb64, token):
        pk = force_str(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.filter(pk=pk).first()
        if account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect("posts:main")
        return render(request, self.template_name)


# Edit
class SettingsView(LoginRequiredMixin, View):
    template_name = "accounts/settings/main.html"
    form_class = forms.AccountEditForm

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=request.user)
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("accounts:settings")
        return render(request, self.template_name, {"form": form})


# View
class AccountDetailView(LoginRequiredMixin, View):
    template_name = "accounts/view/detail.html"
    form_class = forms.AccountDetailForm

    def get(self, request, *args, **kwargs):
        account = get_object_or_404(get_user_model(), pk=kwargs["pk"])
        form = self.form_class(instance=account)
        return render(request, self.template_name, {"form": form})
