from django.contrib import admin

from chat import models


@admin.register(models.Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ("activity", "owner", "candidate", "is_active", "updated_at", "created_at")
    list_filter = ("updated_at", "created_at")
    autocomplete_fields = ("activity", "owner", "candidate")
    readonly_fields = ("uuid", "updated_at", "created_at")
    search_fields = ("uuid", )

    def get_queryset(self, request):
        return models.Thread.objects.all().select_related(
            "activity", "owner", "candidate"
        ).order_by("-updated_at")


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("message", "owner", "thread", "created_at")
    list_filter = ("created_at", )
    autocomplete_fields = ("thread", "owner")
    readonly_fields = ("created_at", )

    def get_queryset(self, request):
        return models.Message.objects.all().select_related(
            "thread", "owner"
        ).order_by("-created_at")
