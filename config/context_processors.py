from django.db.models import Q, Exists, OuterRef

from posts.models import ActivityApply
from chat.models import Thread, Message


def notifications(request):
    if request.user.is_authenticated:
        thread = Thread.objects.filter(
            Q(owner=request.user) | Q(candidate=request.user)
        ).annotate(
            new_messages=Exists(
                Message.objects.filter(~Q(owner=request.user), thread=OuterRef("pk"), is_read=False)
            )
        ).values_list("new_messages", flat=True)
        return {
            "check_replies": ActivityApply.objects.filter(
                status=1, activity__owner=request.user
            ).exists(),
            "check_messages": True in thread,
        }
    else:
        return ""
