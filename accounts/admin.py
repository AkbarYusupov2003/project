from django.contrib import admin
from django.contrib.auth import get_user_model


@admin.register(get_user_model())
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email",  "description", "system_language", "country", "is_active", "is_staff", "is_superuser")
    list_filter = ("system_language", "country")
    autocomplete_fields = ("skills",)
    search_fields = ("username", "email")

    def get_queryset(self, request):
        return get_user_model().objects.all().order_by("-pk")
