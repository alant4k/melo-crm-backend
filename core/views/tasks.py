from rest_framework.viewsets import ModelViewSet
from django.db.models import Q
from rest_framework.permissions import IsAdminUser
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework import serializers
from django_filters.rest_framework import DjangoFilterBackend
from core.models import Task, Tag
from ..serializers import TaskSerializer, TagSerializer
from ..mixins import OwnerPermissionMixin, SaveUserMixin, AdminDestroyPermissionMixin


class TaskViewSet(SaveUserMixin, OwnerPermissionMixin, ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = ["title, user__username"]
    filterset_fields = ["user_id", "status", "closed", "tags__id"]
    ordering_fields = [
        "id",
        "title",
        "updated_at",
        "tags",
        "user",
        "due_date",
        "status",
    ]
    ordering = ["-id"]

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_staff:
            return qs
        return qs.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        if "tags" in request.query_params:
            tags = request.query_params["tags"].split(",")
            self.queryset = qs.filter(tags__id__in=tags)
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        if Task.objects.filter(user=request.user, closed=False).exists():
            raise serializers.ValidationError(
                {
                    "task_error": ["This user already has a task in progress."],
                }
            )
        return super().create(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        if Task.objects.filter(
            user=request.user, closed=True, pk=kwargs["pk"]
        ).exists():
            raise serializers.ValidationError(
                {
                    "task_error": ["This user already has a task closed."],
                }
            )

        return super().update(request, *args, **kwargs)


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = TagSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = ["name"]
    ordering_fields = ["id", "name", "updated_at"]
    ordering = ["-id"]
