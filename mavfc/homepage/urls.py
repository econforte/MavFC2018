from django.conf.urls import url
from . import views

password_urls = [

]

urlpatterns = [
    #url(r'^$', RedirectView.as_view(pattern_name='dj-auth:pw_reset_start', permanent=False)),
    url(r'^$', views.home, name="homepage"),
]
