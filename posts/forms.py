from django import forms
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from mptt.forms import TreeNodeMultipleChoiceField

from posts import models
from posts.utils import LANGUAGES


IS_ONLINE_CHOICES = (
    (True, _("Yes")),
    (False, _("No")),
)

IS_ONLINE_FILTER_CHOICES = (
    ("", _("Any")),
    (True, _("Yes")),
    (False, _("No")),
)


class ActivityForm(forms.ModelForm):
    language = forms.ChoiceField(
        label=_("Language of activity"),
        choices=LANGUAGES,
        widget=forms.Select(
            attrs={
                "class": "form-control selectpicker",
                "data-live-search": "true",
            }
        )
    )
    title = forms.CharField(
        label=_("Title"),
        min_length=8,
        max_length=128,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-2",
                "placeholder": _("From 8 to 128 characters"),
            }
        ),
    )
    type = forms.ChoiceField(
        label=_("Type"),
        choices=models.Activity.TypeChoices.choices,
        widget=forms.Select(
            attrs={
                "class": "form-control mb-2"
            }
        )
    )
    description = forms.CharField(
        label=_("Description"),
        max_length=2048,
        widget=forms.Textarea(
            attrs={
                "class": "form-control mb-2",
                "placeholder": _("Up to 2048 characters"),
                "rows": "2"
            }
        ),
    )
    country = CountryField(
        blank_label=_("Select country")
    ).formfield(
        label=_("Country"),
        widget=forms.Select(attrs={"class": "form-control selectpicker", "data-live-search": "true",})
    )
    is_online = forms.ChoiceField(
        label=_("Is Online"),
        choices=IS_ONLINE_CHOICES,
        widget=forms.Select(attrs={"class": "form-control mb-2"})
    )
    location = forms.CharField(
        label=_("Location"),
        max_length=128,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-2",
                "placeholder": _("Up to 128 characters"),
            }
        )
    )
    programming_areas = TreeNodeMultipleChoiceField(
        label=_("Programming areas"),
        queryset=models.ProgrammingArea.objects.all(),
        level_indicator="•",
        widget=forms.SelectMultiple(
            attrs={
                "class": "form-control selectpicker",
                "data-live-search": "true",
            }
        )
    )
    global_areas = TreeNodeMultipleChoiceField(
        label=_("Global areas"),
        queryset=models.GlobalArea.objects.all(),
        level_indicator="•",
        required=False,
        widget=forms.SelectMultiple(
            attrs={
                "class": "form-control selectpicker",
                "data-live-search": "true",
            }
        )
    )
    expected_skills = TreeNodeMultipleChoiceField(
        label=_("Expected skills"),
        queryset=models.ProgrammingSkill.objects.all(),
        level_indicator="•",
        widget=forms.SelectMultiple(
            attrs={
                "class": "form-control selectpicker",
                "data-live-search": "true",
            }
        )
    )

    class Meta:
        model = models.Activity
        fields = (
            "language", "country", "title", "type", "description", "is_online",
            "location", "programming_areas", "global_areas", "expected_skills"
        )
        widgets = {
            "country": CountrySelectWidget(
                attrs={"class": "form-control mb-2 selectpicker"}
            )
        }


class ActivityReadonlyForm(forms.ModelForm):
    title = forms.CharField(
        label=_("Title"),
        min_length=8,
        max_length=128,
        disabled=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-2",
                "placeholder": _("From 8 to 128 characters"),
            }
        ),
    )
    type = forms.ChoiceField(
        label=_("Type"),
        choices=models.Activity.TypeChoices.choices,
        disabled=True,
        widget=forms.Select(
            attrs={
                "class": "form-control mb-2"
            }
        )
    )
    description = forms.CharField(
        label=_("Description"),
        max_length=2048,
        disabled=True,
        widget=forms.Textarea(
            attrs={
                "class": "form-control mb-2",
                "placeholder": _("Up to 2048 characters"),
                "rows": "2"
            }
        ),
    )
    country = CountryField(
        blank_label=_("Select country")
    ).formfield(
        label=_("Country"),
        disabled=True,
        widget=forms.Select(attrs={"class": "form-control selectpicker", "data-live-search": "true",})
    )
    is_online = forms.ChoiceField(
        label=_("Is Online"),
        choices=IS_ONLINE_CHOICES,
        disabled=True,
        widget=forms.Select(attrs={"class": "form-control mb-2"})
    )
    location = forms.CharField(
        label=_("Location"),
        max_length=128,
        disabled=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-2",
                "placeholder": _("Up to 128 characters"),
            }
        )
    )
    programming_areas = TreeNodeMultipleChoiceField(
        label=_("Programming areas"),
        queryset=models.ProgrammingArea.objects.all(),
        level_indicator="•",
        disabled=True,
        widget=forms.SelectMultiple(
            attrs={
                "class": "form-control selectpicker",
                "data-live-search": "true",
            }
        )
    )
    global_areas = TreeNodeMultipleChoiceField(
        label=_("Global areas"),
        queryset=models.GlobalArea.objects.all(),
        level_indicator="•",
        required=False,
        disabled=True,
        widget=forms.SelectMultiple(
            attrs={
                "class": "form-control selectpicker",
                "data-live-search": "true",
            }
        )
    )
    expected_skills = TreeNodeMultipleChoiceField(
        label=_("Expected skills"),
        queryset=models.ProgrammingSkill.objects.all(),
        level_indicator="•",
        disabled=True,
        widget=forms.SelectMultiple(
            attrs={
                "class": "form-control selectpicker",
                "data-live-search": "true",
            }
        )
    )

    class Meta:
        model = models.Activity
        fields = (
            "country", "title", "type", "description", "is_online", "location",
            "programming_areas", "global_areas", "expected_skills"
        )
        widgets = {
            "country": CountrySelectWidget(
                attrs={"class": "form-control mb-2 selectpicker"}
            )
        }


class ActivityFilterForm(forms.ModelForm):
    language = forms.ChoiceField(
        label=_("Language of activity"),
        required=False,
        choices=LANGUAGES,
        widget=forms.Select(
            attrs={
                "class": "form-control selectpicker",
                "data-live-search": "true",
            }
        )
    )
    country = CountryField(
        blank_label=_("Select country")
    ).formfield(
        label=_("Country"),
        required=False,
        widget=forms.Select(attrs={"class": "form-control selectpicker",
                                   "data-live-search": "true", })
    )
    type = forms.ChoiceField(
        label=_("Type"),
        choices=[('', _("Select type"))] + models.Activity.TypeChoices.choices,
        initial="",
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control mb-2"
            }
        )
    )
    is_online = forms.ChoiceField(
        label=_("Is Online"),
        choices=IS_ONLINE_FILTER_CHOICES,
        required=False,
        widget=forms.Select(attrs={"class": "form-control mb-2"})
    )
    programming_areas = TreeNodeMultipleChoiceField(
        label=_("Programming areas"),
        queryset=models.ProgrammingArea.objects.all(),
        level_indicator="•",
        required=False,
        widget=forms.SelectMultiple(
            attrs={
                "class": "form-control selectpicker",
                "data-live-search": "true",
            }
        )
    )
    global_areas = TreeNodeMultipleChoiceField(
        label=_("Global areas"),
        queryset=models.GlobalArea.objects.all(),
        level_indicator="•",
        required=False,
        widget=forms.SelectMultiple(
            attrs={
                "class": "form-control selectpicker",
                "data-live-search": "true",
            }
        )
    )
    expected_skills = TreeNodeMultipleChoiceField(
        label=_("Expected skills"),
        queryset=models.ProgrammingSkill.objects.all(),
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
        model = models.Activity
        fields = (
            "language", "country", "type", "is_online",
            "programming_areas", "global_areas", "expected_skills"
        )
        widgets = {
            "country": CountrySelectWidget(
                attrs={"class": "form-control mb-2 selectpicker"}
            )
        }
