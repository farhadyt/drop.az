# core/urls.py
from django.contrib import admin
from django.urls import path, include
# Bu iki sətri import edirik
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('catalog.urls')),
]

# Bu hissəni ən sona əlavə edirik
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)