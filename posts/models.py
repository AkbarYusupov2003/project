from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from django_countries.fields import CountryField

from posts.utils import LANGUAGES


class GlobalArea(MPTTModel):
    parent = TreeForeignKey(
        "self",
        verbose_name=_("Parent"),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
    )
    name = models.CharField(_("Name"), max_length=255)

    class Meta:
        verbose_name = "Global Area"
        verbose_name_plural = "Global Areas"

    class MPTTMeta:
        order_insertion_by = ("name",)

    def __str__(self):
        return self.name


class ProgrammingArea(MPTTModel):
    parent = TreeForeignKey(
        "self",
        verbose_name=_("Parent"),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
    )
    name = models.CharField(_("Name"), max_length=255)

    class Meta:
        verbose_name = "Programming Area"
        verbose_name_plural = "Programming Areas"

    class MPTTMeta:
        order_insertion_by = ("name",)

    def __str__(self):
        return self.name


class ProgrammingSkill(MPTTModel):
    parent = TreeForeignKey(
        "self",
        verbose_name=_("Parent"),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
    )
    name = models.CharField(_("Name"), max_length=128)

    class Meta:
        verbose_name = "Programming Skill"
        verbose_name_plural = "Programming Skills"

    class MPTTMeta:
        order_insertion_by = ("name",)

    def __str__(self):
        return self.name


class ActivityManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class Activity(models.Model):
    class TypeChoices(models.IntegerChoices):
        project_based = 1, _("Project Development")
        learning = 2, _("Collaborative Learning")
        problem_solving = 3, _("Problem-Solving")

    owner = models.ForeignKey(
        get_user_model(),
        verbose_name=_("Owner"),
        on_delete=models.CASCADE
    )
    language = models.PositiveIntegerField(
        verbose_name=_("Language"),
        choices=LANGUAGES
    )
    title = models.CharField(_("Title"), max_length=128)
    type = models.PositiveIntegerField(
        verbose_name=_("Type"), choices=TypeChoices.choices
    )
    description = models.TextField(verbose_name=_("Description"), max_length=2048)
    programming_areas = models.ManyToManyField(
        ProgrammingArea, verbose_name=_("Programming Area")
    )
    global_areas = models.ManyToManyField(
        GlobalArea, verbose_name=_("Global Area")
    )
    expected_skills = models.ManyToManyField(
        ProgrammingSkill, verbose_name=_("Expected skills")
    )
    is_online = models.BooleanField(verbose_name=_("Is Online"), default=True)
    country = CountryField(verbose_name=_("Country"))
    location = models.CharField(_("Location"), max_length=128, null=True, blank=True)
    updated_at = models.DateTimeField(
        verbose_name=_("Updated at"), auto_now=True
    )
    created_at = models.DateTimeField(
        verbose_name=_("Created at"),
        auto_now_add=True
    )
    is_deleted = models.BooleanField(verbose_name=_("Is Deleted"), default=False)
    objects = ActivityManager()
    with_deleted = models.Manager()

    class Meta:
        verbose_name = "Activity"
        verbose_name_plural = "Activities"

    def __str__(self):
        return self.title


class ActivityApply(models.Model):
    class StatusChoices(models.IntegerChoices):
        project_based = 1, _("Sent")
        accepted = 2, _("Accepted")
        rejected = 3, _("Rejected")

    owner = models.ForeignKey(
        get_user_model(),
        verbose_name=_("Owner"),
        on_delete=models.CASCADE,
    )
    status = models.PositiveIntegerField(
        verbose_name=_("Status"), choices=StatusChoices.choices, default=1
    )
    comment = models.CharField(max_length=512, null=True, blank=True)
    activity = models.ForeignKey(
        Activity,
        verbose_name=_("Activity"),
        on_delete=models.CASCADE
    )
    updated_at = models.DateTimeField(
        verbose_name=_("Updated at"), auto_now=True
    )
    created_at = models.DateTimeField(
        verbose_name=_("Created at"),
        auto_now_add=True
    )

    class Meta:
        verbose_name = "Activity Apply"
        verbose_name_plural = "Activity Applies"


class ActivityReport(models.Model):
    class ReasonChoices(models.IntegerChoices):
        unacceptable_content = 1, _("Unacceptable content")
        fraud = 2, _("Fraud")
        not_match = 3, _("Language and activity does not match")

    owner = models.ForeignKey(
        get_user_model(),
        verbose_name=_("Owner"),
        on_delete=models.CASCADE
    )
    reason = models.PositiveIntegerField(
        verbose_name=_("Type"), choices=ReasonChoices.choices
    )
    message = models.CharField(max_length=255)
    activity = models.ForeignKey(
        Activity,
        verbose_name=_("Activity"),
        on_delete=models.CASCADE
    )
    updated_at = models.DateTimeField(
        verbose_name=_("Updated at"), auto_now=True
    )
    created_at = models.DateTimeField(
        verbose_name=_("Created at"),
        auto_now_add=True
    )
    is_checked = models.BooleanField(
        verbose_name=_("Is Checked"), default=False
    )

    class Meta:
        verbose_name = "Activity Report"
        verbose_name_plural = "Activity Reports"

    def __str__(self):
        return self.message
