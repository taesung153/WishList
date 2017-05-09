from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register$', views.register, name = 'register'),
    url(r'^login$', views.login, name = 'login'),
    url(r'^addWish$', views.addWish, name = 'addWish'),
    url(r'^delWish/(?P<id>)$', views.delWish, name = 'delWish'),
    url(r'^mvWish$', views.mvWish, name = 'mvWish'),
    url(r'^showWish/(?P<id>)$', views.showWish, name = 'showWish'),
    url(r'^logOut$', views.logOut, name = 'logOut'),
]
