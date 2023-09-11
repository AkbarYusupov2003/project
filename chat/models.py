import uuid
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from posts.models import Activity


class Thread(models.Model):
    uuid = models.UUIDField(
        unique=True, default=uuid.uuid4, db_index=True, editable=False
    )
    activity = models.ForeignKey(
        Activity,
        verbose_name=_("Activity"),
        on_delete=models.CASCADE
    )
    owner = models.ForeignKey(
        get_user_model(),
        verbose_name=_("Owner"),
        on_delete=models.CASCADE,
        related_name="owner",
    )
    candidate = models.ForeignKey(
        get_user_model(),
        verbose_name=_("Candidate"),
        on_delete=models.CASCADE,
        related_name="candidate",
    )
    updated_at = models.DateTimeField(
        verbose_name=_("Updated at"), auto_now=True
    )
    created_at = models.DateTimeField(
        verbose_name=_("Created at"), auto_now_add=True
    )
    is_active = models.BooleanField(verbose_name=_("Is Active"), default=True)

    class Meta:
        verbose_name = "Thread"
        verbose_name_plural = "Threads"


class Message(models.Model):
    thread = models.ForeignKey(
        Thread,
        verbose_name=_("Thread"),
        on_delete=models.CASCADE,
        related_name="messages",
    )
    owner = models.ForeignKey(
        get_user_model(), verbose_name=_("Owner"), on_delete=models.CASCADE
    )
    message = models.CharField(verbose_name=_("Message"), max_length=2048)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
