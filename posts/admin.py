from django.urls import reverse_lazy
from django.utils.html import format_html
from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from posts import models


@admin.register(models.GlobalArea)
class GlobalAreaAdmin(MPTTModelAdmin):
    list_display = ("name", )
    search_fields = ("name",)


@admin.register(models.ProgrammingArea)
class ProgrammingAreaAdmin(MPTTModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(models.ProgrammingSkill)
class ProgrammingSkillAdmin(MPTTModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(models.Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "language",  "type", "description", "updated_at", "is_deleted")
    list_filter = ("type", "language")
    autocomplete_fields = ("owner", "programming_areas", "global_areas", "expected_skills")
    search_fields = ("title", "description")
    readonly_fields = ("updated_at", "created_at")

    def get_queryset(self, request):
        return models.Activity.with_deleted.all().select_related(
            "owner"
        ).order_by("is_deleted", "-updated_at")


@admin.register(models.ActivityApply)
class ActivityApplyAdmin(admin.ModelAdmin):
    list_display = ("status", "owner", "comment", "activity", "updated_at")
    list_filter = ("status", "created_at")
    autocomplete_fields = ("owner", "activity")
    search_fields = ("comment",)
    readonly_fields = ("updated_at", "created_at")

    def get_queryset(self, request):
        return models.ActivityApply.objects.all().select_related(
            "owner", "activity"
        ).order_by("-updated_at")


@admin.register(models.ActivityReport)
class ActivityReportAdmin(admin.ModelAdmin):
    list_display = ("reason", "owner", "message", "activity", "is_checked", "updated_at")
    list_filter = ("is_checked", "reason")
    autocomplete_fields = ("owner", "activity")
    search_fields = ("message",)
    readonly_fields = ("updated_at", "created_at")

    @staticmethod
    def owner(obj):
        link = reverse_lazy(
            "admin:accounts_user_change", args=(obj.owner.pk, )
        )
        return format_html('<a href="{}">{}</a>', link, obj.owner.username)

    @staticmethod
    def activity(obj):
        link = reverse_lazy(
            "admin:posts_activity_change", args=(obj.activity.pk,)
        )
        return format_html('<a href="{}">{}</a>', link, obj.activity.title)

    def get_queryset(self, request):
        return models.ActivityReport.objects.all().select_related(
            "owner", "activity"
        ).order_by("is_checked", "updated_at")
