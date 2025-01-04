from django.urls import path
from .views import *

urlpatterns = [
    path("ping/", PingView.as_view()),
    path("", ApiPageView.as_view()),
]
