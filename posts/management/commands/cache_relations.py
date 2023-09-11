from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _


class Command(BaseCommand):
    """
    The command caches GlobalArea, ProgrammingArea, ProgrammingSkill models
    """

    def handle(self, *args, **options):
        """
        Caching querysets in Redis
        """
        # cache.set("global_areas", models.GlobalArea.objects.all())
        # cache.set("programming_areas", models.ProgrammingArea.objects.all())
        # cache.set("programming_skills", models.ProgrammingSkill.objects.all())
        self.stdout.write(_("The data has been successfully cached"))
