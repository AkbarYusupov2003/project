from django.urls import path

from posts import views


app_name = "posts"

urlpatterns = [
    # Main
    path("", views.MainView.as_view(), name="main"),
    # Activity Detail
    path("activity/<int:pk>/", views.ActivityDetailView.as_view(), name="activity-detail"),
    # Apply
    path("activity-reply/", views.ActivityReplyCreateView.as_view()),
    # Report
    path("activity-report/", views.ActivityReportCreateView.as_view()),
    # Activity Owner
    path("my-activities/", views.OwnerActivityListView.as_view(), name="owner-activity-list"),
    path("my-activities/create/", views.OwnerActivityCreateView.as_view(), name="owner-activity-create"),
    path("my-activities/<int:pk>/", views.OwnerActivityDetailView.as_view(), name="owner-activity-detail"),
    path("my-activities/delete/<int:pk>/", views.OwnerActivityDeleteView.as_view(), name="owner-activity-delete"),
    # Manage Requests
    path("manage/", views.ManageListView.as_view(), name="manage-list"),
    path("manage/accept/", views.ManageAcceptView.as_view()),
    path("manage/reject/", views.ManageRejectView.as_view()),
    # Explanatory Information
    path("about/", views.AboutProjectView.as_view(), name="about"),
    path("sections/", views.SectionsView.as_view(), name="sections"),
    # How To use
]
