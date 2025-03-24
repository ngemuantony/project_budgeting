from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.views.decorators.cache import cache_control
from django.views.static import serve
from pwa import views as pwa_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("", include("app.urls")),
    path("users/", include("users.urls", namespace="users")),
    # Offline page with caching
    path('offline/', cache_control(max_age=86400)(TemplateView.as_view(
        template_name='offline.html',
        content_type='text/html',
    )), name='offline'),
    
    # Serve static files in production
    path('static/<str:path>', serve, {'document_root': settings.STATIC_ROOT}),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Add static and media serving for development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Admin site customization
SITE_NAME = "Project Management System"
admin.site.site_header = SITE_NAME
admin.site.index_title = f"{SITE_NAME} Dashboard"
admin.site.site_title = f"{SITE_NAME} Dashboard"