import os
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from portfolio import views as portfolio_views

handler404 = portfolio_views.handler404
handler500 = portfolio_views.handler500

ADMIN_URL = os.environ.get("ADMIN_URL", "admin") + "/"

urlpatterns = [
    path(ADMIN_URL, admin.site.urls),
    path("", include("portfolio.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)