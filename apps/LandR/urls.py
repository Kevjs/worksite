from django.conf.urls import url
from . import views

urlpatterns =[
    url(r'^$', views.home, name="home"),
    url(r'^login$', views.login, name="login"),
    url(r'^logout$', views.logout, name="logout"),
    url(r'^first$', views.first, name="first"),
    url(r'^firtProcessing$', views.firstP, name="firstP"),
]