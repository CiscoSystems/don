from django.conf.urls import url
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/static/don.html')),
    url(r'^test/$', views.test, name='test'),
    url(r'^view/$', views.view, name='view'),
    url(r'^analyze/$', views.analyze, name='analyze'),
    url(r'^ping/$', views.ping, name='ping'),
]
