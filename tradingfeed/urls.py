"""
URL configuration for tradingfeed project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("authentication.urls", namespace="authentication_app")),
    path("pricing/", include("subscription.urls", namespace="subscription_app")),
    path("accounts/", include("django.contrib.auth.urls")), 
    path("", include("home.urls")),
    path("broadcasting/", include("broadcasting.urls")),
    path("", include("alerts.urls")),
    path(
        "broadcasting/", include("broadcasting.urls")
    ),
    path("", include("bookmark.urls")),
    path("", include("userProfile.urls")),
]
# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
