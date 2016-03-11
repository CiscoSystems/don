from django.conf.urls import url
from django.views.generic import RedirectView,TemplateView

from . import views

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='don.html')),
    url(r'^test/$', views.test, name='test'),
    url(r'^view/$', views.view, name='view'),
    url(r'^analyze/$', views.analyze, name='analyze'),
    url(r'^ping/$', views.ping, name='ping'),
    url(r'^collect/$', views.collect, name='collect'),
]
