from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from config import settings


APPS_URLS = [
    path('admin/', admin.site.urls),
]

MEDIA_URLS = [static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
              static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
              ]


urlpatterns = APPS_URLS

# TODO: Add media URLs
# if settings.DEBUG:
# #     urlpatterns += MEDIA_URLS
