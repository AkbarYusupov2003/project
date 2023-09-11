from django.urls import path

from chat import views


app_name = "chat"

urlpatterns = [
    path("", views.MainView.as_view(), name="main"),
    path("<uuid:uuid>/", views.ThreadView.as_view(), name="thread"),
]
