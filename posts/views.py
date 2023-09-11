import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.humanize.templatetags import humanize
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views import View, generic
from django.views.decorators.csrf import csrf_exempt

from chat.models import Thread
from posts import models
from posts import forms
from posts import filters


# Main
class MainView(LoginRequiredMixin, generic.ListView):
    template_name = "posts/main.html"
    paginate_by = 20

    def get(self, request, *args, **kwargs):
        reported = models.ActivityReport.objects.filter(
            owner=request.user
        ).values_list('activity__pk', flat=True)
        applied = models.ActivityApply.objects.filter(
            owner=request.user
        ).values_list('activity__pk', flat=True)
        excluded = [*reported, *applied]
        queryset = models.Activity.objects.all().exclude(Q(pk__in=excluded) | Q(owner=request.user))

        if len(request.GET) >= 4:
            f = filters.ActivityFilter(data=request.GET, queryset=queryset)
        else:
            qs = queryset.filter(country=request.user.country)
            f = filters.ActivityFilter(queryset=qs, country=request.user.country)

        for activity in f.qs:
            activity.updated_at = humanize.naturaltime(activity.updated_at)

        self.object_list = f.qs.order_by("-updated_at").prefetch_related(
            "programming_areas", "global_areas", "expected_skills"
        ).select_related("owner")
        return render(
            request,
            self.template_name,
            {"filter": f, **self.get_context_data()}
        )


# Activity Detail
class ActivityDetailView(LoginRequiredMixin, View):
    template_name = "posts/activity/view/detail.html"
    form_class = forms.ActivityReadonlyForm

    def get(self, request, *args, **kwargs):
        activity = get_object_or_404(
            models.Activity.with_deleted, pk=kwargs["pk"]
        )
        if activity.is_deleted:
            return render(request, "posts/activity/view/deleted.html")
        else:
            form = self.form_class(instance=activity)
            return render(request, self.template_name, {"form": form})


# Apply
class ActivityReplyCreateView(LoginRequiredMixin, View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        body = json.loads(request.body)
        try:
            pk = int(body.get("reply_pk"))
            comment = str(body.get("reply_comment"))
            activity = get_object_or_404(models.Activity, pk=pk)
            if activity.owner != request.user:
                models.ActivityApply.objects.create(
                    owner=request.user, comment=comment, activity=activity
                )
        except:
            pass
        finally:
            return HttpResponse("")


# Report
class ActivityReportCreateView(LoginRequiredMixin, View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        body = json.loads(request.body)
        try:
            pk = int(body.get("report_pk"))
            reason = int(body.get("report_reason"))
            message = str(body.get("report_message"))
            activity = get_object_or_404(models.Activity, pk=pk)
            if activity.owner != request.user:
                models.ActivityReport.objects.create(
                    owner=request.user, reason=reason, message=message, activity=activity
                )
        except:
            pass
        finally:
            return HttpResponse("")


# Activity Owner
class OwnerActivityListView(LoginRequiredMixin, generic.ListView):
    template_name = "posts/activity/owner/list.html"
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        activities = self.get_queryset()
        for activity in activities:
            activity.updated_at = humanize.naturaltime(activity.updated_at)
        self.object_list = activities
        return render(request, self.template_name, {**self.get_context_data()})

    def get_queryset(self):
        return models.Activity.objects.filter(
            owner=self.request.user
        ).order_by("-updated_at")


class OwnerActivityCreateView(LoginRequiredMixin, View):
    template_name = "posts/activity/owner/create.html"
    form_class = forms.ActivityForm

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.owner = request.user
            activity.save()
            form.save_m2m()
            return redirect("posts:owner-activity-list")
        return render(request, self.template_name, {"form": form})


class OwnerActivityDetailView(LoginRequiredMixin, View):
    template_name = "posts/activity/owner/detail.html"
    form_class = forms.ActivityForm

    def get(self, request, *args, **kwargs):
        activity = get_object_or_404(
            models.Activity, pk=kwargs["pk"], owner=request.user
        )
        form = self.form_class(instance=activity)
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        activity = get_object_or_404(
            models.Activity, pk=kwargs["pk"], owner=request.user
        )
        form = self.form_class(request.POST, instance=activity)
        if form.is_valid():
            form.save()
            return redirect("posts:owner-activity-list")
        return render(request, self.template_name, {"form": form})


class OwnerActivityDeleteView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        activity = get_object_or_404(
            models.Activity, pk=kwargs["pk"], owner=request.user
        )
        activity.is_deleted = True
        activity.save()
        return redirect("posts:owner-activity-list")


# Manage Responds
class ManageListView(LoginRequiredMixin, generic.ListView):
    template_name = "posts/activity/manage/list.html"
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        if request.GET.get("status") == "up_to_you":
            queryset = models.ActivityApply.objects.filter(
                activity__owner=self.request.user, status=1
            ).select_related("owner", "activity")
        else:
            queryset = self.get_queryset()

        for obj in queryset:
            obj.updated_at = humanize.naturaltime(obj.updated_at)
            if obj.status == 1 and obj.owner != self.request.user:
                obj.status = _("Up to you")
                obj.decide = True
            if not obj.comment:
                obj.comment = _("Not entered")
        self.object_list = queryset
        return render(request, self.template_name, {**self.get_context_data()})

    def get_queryset(self):
        to_you = models.ActivityApply.objects.filter(activity__owner=self.request.user).select_related("owner", "activity")
        from_you = models.ActivityApply.objects.filter(owner=self.request.user).select_related("owner", "activity")
        return to_you.union(from_you).order_by("-updated_at")


class ManageAcceptView(LoginRequiredMixin, View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        body = json.loads(request.body)
        try:
            pk = int(body.get("activity_pk"))
            apply = get_object_or_404(
                models.ActivityApply.objects.select_related("activity", "activity__owner"),
                pk=pk, activity__owner=request.user, status=1
            )
            with transaction.atomic():
                apply.status = 2
                apply.save()
                Thread.objects.create(
                    activity=apply.activity, owner=request.user, candidate=apply.owner
                )
        except:
            pass
        finally:
            return HttpResponse("")


class ManageRejectView(LoginRequiredMixin, View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        body = json.loads(request.body)
        try:
            pk = int(body.get("activity_pk"))
            activity = get_object_or_404(
                models.ActivityApply, pk=pk, activity__owner=request.user, status=1
            )
            activity.status = 3
            activity.save()
        except:
            pass
        finally:
            return HttpResponse("")


# Explanatory Information
class AboutProjectView(LoginRequiredMixin, View):
    template_name = "info/about.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class SectionsView(LoginRequiredMixin, View):
    template_name = "info/sections.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
