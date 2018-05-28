from django.urls import path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.CustomUserViewSet)
router.register(r'members', views.SiteUserViewSet)

user_api_urls = [
    path('users/', views.CustomUserViewSet.as_view({'get': 'list'}), name='customuser_api'),
    path('members/', views.SiteUserViewSet.as_view({'get': 'list'}), name='siteuser_api'),
]
