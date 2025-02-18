from django.urls import path

from core.views import (
    ClientViewSet,
    ContactViewSet,
    CategoryViewSet,
    PositionViewSet,
    SaleViewSet,
    SaleHistoryViewSet,
    TaskViewSet,
    TagViewSet,
)
from .views.base import *
from rest_framework.routers import SimpleRouter


app_name = "core"

clients_router = SimpleRouter()
clients_router.register("clients", ClientViewSet, basename="clients-api")

contacts_router = SimpleRouter()
contacts_router.register("contacts", ContactViewSet, basename="contacts-api")

categories_router = SimpleRouter()
categories_router.register("categories", CategoryViewSet, basename="categories-api")

positions_router = SimpleRouter()
positions_router.register("positions", PositionViewSet, basename="positions-api")

sales_router = SimpleRouter()
sales_router.register("sales", SaleViewSet, basename="sales-api")

sales_history_router = SimpleRouter()
sales_history_router.register(
    "sales-history", SaleHistoryViewSet, basename="sales-history-api"
)

tasks_router = SimpleRouter()
tasks_router.register("tasks", TaskViewSet, basename="tasks-api")

tags_router = SimpleRouter()
tags_router.register("tags", TagViewSet, basename="tags-api")


urlpatterns = [
    # Public Routes
    path("ping/", PingView.as_view(), name="ping"),
    path("", ApiPageView.as_view(), name="api_index"),
]

urlpatterns += clients_router.urls
urlpatterns += contacts_router.urls
urlpatterns += categories_router.urls
urlpatterns += positions_router.urls
urlpatterns += sales_router.urls
urlpatterns += sales_history_router.urls
urlpatterns += tasks_router.urls
urlpatterns += tags_router.urls
