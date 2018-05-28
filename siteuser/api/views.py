from rest_framework import viewsets
from ..models import CustomUser, SiteUser
from .import serializers

class SiteUserViewSet(viewsets.ModelViewSet):
    queryset = SiteUser.objects.all().order_by('created')
    serializer_class = serializers.SiteUserSerializer

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = serializers.CustomUserSerializer
