from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^score$', views.score, name='score'),
    url(r'^logout$', views.logout_view, name='logout')
]