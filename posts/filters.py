import django_filters

from posts import models
from posts import forms


class ActivityFilter(django_filters.FilterSet):

    class Meta:
        model = models.Activity
        fields = ("language", "type", "programming_areas", "global_areas", "expected_skills", "is_online", "country")
        form = forms.ActivityFilterForm

    def __init__(self, data=None, country=None, **kwargs):
        self.country = country
        super().__init__(data, **kwargs)

    @property
    def form(self):
        if not hasattr(self, "_form"):
            if self.is_bound:
                form = self._meta.form
                self._form = form(self.data)
            elif self.country:
                form = self._meta.form()
                form.fields["country"].initial = self.country
                self._form = form
            else:
                self._form = self._meta.form
        return self._form
