"""voidcoin URL Configuration"""

from django.urls import include, path
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static

from .import views

urlpatterns = [
    path("", include('chain.urls')),
    path('getting-started/', views.read_me),
    path("user/", include('siteuser.urls')),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += path("__debug__/", include(debug_toolbar.urls)),
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
