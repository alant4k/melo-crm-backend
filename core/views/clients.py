from core.models import Client
from ..serializers import ClientSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated


class ClientViewSet(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "options", "head", "post", "patch", "delete"]

    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.order_by("-updated_at")
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(edited_by=self.request.user)
        return super().perform_update(serializer)
