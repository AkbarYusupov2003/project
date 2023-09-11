from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from timezone_field import TimeZoneFormField
from mptt.forms import TreeNodeMultipleChoiceField

from accounts.tasks import send_password_reset_email_task
from posts.models import ProgrammingSkill


class RegisterForm(forms.ModelForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": _("Enter the email"),
            }
        ),
    )
    username = forms.CharField(
        label=_("Username"),
        min_length=4,
        max_length=32,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": _("From 4 to 32 characters"),
            }
        ),
    )
    country = CountryField(
        blank_label=_("Select country")
    ).formfield(
        label=_("Country"),
        widget=forms.Select(attrs={"class": "form-control selectpicker", "data-live-search": "true",})
    )
    timezone = TimeZoneFormField(
        initial="UTC",
        choices_display="WITH_GMT_OFFSET",
        widget=forms.Select(
            attrs={
                "class": "form-control selectpicker border",
                "data-live-search": "true",
            }
        )
    )
    system_language = forms.ChoiceField(
        label=_("System Language"),
        choices=get_user_model().LanguageChoices.choices,
        widget=forms.Select(
            attrs={
                "class": "form-control mb-3",
            }
        )
    )
    password1 = forms.CharField(
        label=_("Password"),
        min_length=8,
        max_length=64,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": _("From 8 to 64 characters"),
            }
        ),
    )
    password2 = forms.CharField(
        label=_("Repeat Password"),
        min_length=8,
        max_length=64,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": _("From 8 to 64 characters"),
            }
        ),
    )

    class Meta:
        model = get_user_model()
        fields = ("email", "username", "country", "timezone", "system_language", "password1", "password2")

    def clean_password2(self):
        if self.cleaned_data["password1"] == self.cleaned_data["password2"]:
            return self.cleaned_data["password2"]
        else:
            raise forms.ValidationError(_("Passwords are different"))


class LoginForm(forms.Form):
    email = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": _("Enter the email"),
            }
        ),
    )
    password = forms.CharField(
        label=_("Password"),
        min_length=4,
        max_length=64,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": _("Enter the password"),
            }
        ),
    )


class PwdResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=254,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": _("Email"),
            }
        ),
    )

    def clean_email(self):
        email = self.cleaned_data["email"]
        if get_user_model().objects.filter(email=email).exists():
            return email
        raise forms.ValidationError(
            _("Unfortunately we can not find that email address")
        )

    def send_mail(
        self,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None,
    ):
        context["user"] = ""
        send_password_reset_email_task.delay(context)


class PwdResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("New Password"),
        min_length=8,
        max_length=64,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": _("From 8 to 64 characters"),
            }
        ),
    )
    new_password2 = forms.CharField(
        label=_("Repeat Password"),
        min_length=8,
        max_length=64,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": _("From 8 to 64 characters"),
            }
        ),
    )


class AccountEditForm(forms.ModelForm):
    email = forms.EmailField(
        label=_("Email"),
        disabled=True,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": _("Enter the email"),
            }
        ),
    )
    username = forms.CharField(
        label=_("Username"),
        disabled=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": _("From 4 to 32 characters"),
            }
        ),
    )
    country = CountryField(
        blank_label=_("Select country")
    ).formfield(
        label=_("Country"),
        widget=forms.Select(attrs={"class": "form-control selectpicker", "data-live-search": "true",})
    )
    timezone = TimeZoneFormField(
        choices_display="WITH_GMT_OFFSET",
        widget=forms.Select(
            attrs={
                "class": "form-control selectpicker border",
                "data-live-search": "true",
            }
        )
    )
    system_language = forms.ChoiceField(
        label=_("System Language"),
        choices=get_user_model().LanguageChoices.choices,
        widget=forms.Select(
            attrs={
                "class": "form-control mb-3",
            }
        )
    )
    description = forms.CharField(
        label=_("Description"),
        max_length=2048,
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-control mb-2",
                "placeholder": _("Up to 2048 characters"),
                "rows": "2"
            }
        ),
    )
    skills = TreeNodeMultipleChoiceField(
        label=_("Your Skills"),
        queryset=ProgrammingSkill.objects.all(),
        level_indicator="•",
        required=False,
        widget=forms.SelectMultiple(
            attrs={
                "class": "form-control selectpicker",
                "data-live-search": "true",
            }
        )
    )

    class Meta:
        model = get_user_model()
        fields = ("email", "username", "country", "timezone", "system_language", "description", "skills")


class AccountDetailForm(forms.ModelForm):
    username = forms.CharField(
        label=_("Username"),
        min_length=4,
        max_length=64,
        disabled=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": _("From 4 to 64 characters"),
            }
        ),
    )
    description = forms.CharField(
        label=_("Description"),
        max_length=2048,
        disabled=True,
        widget=forms.Textarea(
            attrs={
                "class": "form-control mb-2",
                "placeholder": _("Empty"),
                "rows": "2"
            }
        ),
    )
    skills = TreeNodeMultipleChoiceField(
        label=_("Skills"),
        queryset=ProgrammingSkill.objects.all(),
        level_indicator="•",
        disabled=True,
        widget=forms.SelectMultiple(
            attrs={
                "class": "form-control selectpicker",
            }
        )
    )

    class Meta:
        model = get_user_model()
        fields = ("username", "description", "skills")
