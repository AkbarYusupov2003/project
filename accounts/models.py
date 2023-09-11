from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField

from timezone_field import TimeZoneField


class UserManager(BaseUserManager):
    def create_superuser(self, email, password, **other_fields):
        other_fields.setdefault("is_active", True)
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)

        if not other_fields.get("is_staff"):
            raise ValueError("Superuser must be assigned to is_staff=True")

        elif not other_fields.get("is_superuser"):
            raise ValueError("Superuser must be assigned to is_superuser=True")

        return self.create_user(email, password, **other_fields)

    def create_user(self, email, password, **other_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **other_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractUser):
    class LanguageChoices(models.TextChoices):
        english = "en", "English"
        russian = "ru", "Русский"

    first_name = None
    last_name = None
    email = models.EmailField(verbose_name=_("Email"), unique=True)
    timezone = TimeZoneField(
        verbose_name=_("Timezone"),
        default="UTC",
        choices_display="WITH_GMT_OFFSET",
        use_pytz=True
    )
    system_language = models.CharField(
        verbose_name=_("System Language"),
        max_length=64,
        choices=LanguageChoices.choices,
        default="English"
    )
    country = CountryField(verbose_name=_("Country"),)
    description = models.TextField(
        max_length=2048, verbose_name=_("Description"), null=True, blank=True
    )
    skills = models.ManyToManyField(
        "posts.ProgrammingSkill", verbose_name=_("Skills"), blank=True
    )
    is_active = models.BooleanField(
        _("active"),
        default=False,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("username", "country")

    def __str__(self):
        return self.username
