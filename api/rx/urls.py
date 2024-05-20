from django.urls import path

from rx.views import Overview


app_name = "rx"
urlpatterns = [
    path("", Overview.as_view(), name="overview"),
]
