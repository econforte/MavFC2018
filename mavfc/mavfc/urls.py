"""mavfc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
#from django.contrib.auth import urls as auth_urls
from user import urls as user_urls
from django.contrib.flatpages import urls as flatpage_urls
from django.contrib.staticfiles import views
from rest_framework.authtoken import views as rest_auth_views
import experiment

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^user/', include(user_urls, app_name='user', namespace='dj-auth')),
    url(r'^food-computer/', include("foodcomputer.urls")),
    url(r'^experiment/', include("experiment.urls")),
    url(r'^media/(?P<path>.*)$', views.serve),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', rest_auth_views.obtain_auth_token),
    # All other URLs should be placed above this line.
    url(r'^', include(flatpage_urls)),
]
