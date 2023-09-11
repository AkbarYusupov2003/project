import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, OuterRef, Exists, Q, Count
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from chat import models


class MainView(LoginRequiredMixin, View):
    template_name = "chat/main.html"

    def get(self, request, *args, **kwargs):
        threads = self.user_threads(request)
        return render(request, self.template_name, {"threads": threads})

    @staticmethod
    def user_threads(request):
        owner = models.Thread.objects.filter(owner=request.user).annotate(
            new_messages=Count(
                models.Message.objects.filter(~Q(owner=request.user), thread=OuterRef("pk"), is_read=False).values_list('id', flat=True)
            ),
            username=F("candidate__username")
        )
        candidate = models.Thread.objects.filter(candidate=request.user).annotate(
            new_messages=Count(
                models.Message.objects.filter(~Q(owner=request.user), thread=OuterRef("pk"), is_read=False).values_list('id', flat=True)
            ),
            username=F("owner__username")
        )
        return owner.union(candidate).order_by("-updated_at")


class ThreadView(LoginRequiredMixin, View):
    template_name = "chat/thread.html"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    @staticmethod
    def user_threads(request, current_thread):
        owner = models.Thread.objects.filter(owner=request.user).annotate(
            new_messages=Count(
                models.Message.objects.filter(~Q(owner=request.user), thread=OuterRef("pk"), is_read=False).values_list('id', flat=True)
            ),
            username=F("candidate__username")
        ).exclude(pk=current_thread.pk)
        candidate = models.Thread.objects.filter(candidate=request.user).annotate(
            new_messages=Count(
                models.Message.objects.filter(~Q(owner=request.user), thread=OuterRef("pk"), is_read=False).values_list('id', flat=True)
            ),
            username=F("owner__username")
        ).exclude(pk=current_thread.pk)
        return owner.union(candidate).order_by("-updated_at")

    def get(self, request, *args, **kwargs):
        current_thread = get_object_or_404(
            models.Thread.objects.select_related("owner", "candidate", "activity"),
            Q(owner=request.user) | Q(candidate=request.user), uuid=kwargs["uuid"],
        )
        if current_thread.owner == request.user:
            buddy = current_thread.candidate
        else:
            buddy = current_thread.owner
        threads = self.user_threads(request, current_thread)
        current_messages = current_thread.messages.all().select_related("owner").order_by("created_at")
        current_messages.filter(
            ~Q(owner=request.user), is_read=False
        ).update(is_read=True)
        context = {
            "threads": threads,
            "current_thread": current_thread,
            "buddy": buddy,
            "current_messages": current_messages,
        }
        if current_thread.is_active:
            return render(request, self.template_name, context)
        else:
            return render(
                request,
                "chat/readonly_thread.html",
                context
            )

    def post(self, request, *args, **kwargs):
        body = json.loads(request.body)
        if body.get("thread_status") == "deactivate":
            thread = get_object_or_404(
                models.Thread,
                Q(owner=request.user) | Q(candidate=request.user), uuid=kwargs["uuid"],
            )
            thread.is_active = False
            thread.save()
        try:
            if int(body.get("message_pk")):
                thread = get_object_or_404(
                    models.Thread,
                    Q(owner=request.user) | Q(candidate=request.user),
                    uuid=kwargs["uuid"],
                )
                message = get_object_or_404(
                    models.Message,
                    ~Q(owner=request.user), thread=thread, pk=int(body.get("message_pk"))
                )
                message.is_read = True
                message.save()
        except:
            pass
        return HttpResponse("")
