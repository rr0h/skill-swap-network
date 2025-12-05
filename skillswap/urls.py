"""
URL configuration for skillswap project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/dashboard/', permanent=False), name='home'),
    path('users/', include('users.urls')),
    path('skills/', include('skills.urls')),
    path('requests/', include('requests.urls')),
    path('reviews/', include('reviews.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('notifications/', include('notifications.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Admin site customization
admin.site.site_header = "Skill Swap Network Admin"
admin.site.site_title = "Skill Swap Admin Portal"
admin.site.index_title = "Welcome to Skill Swap Network Administration"
