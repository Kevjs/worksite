from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name="home"),
    url(r'^messages$', views.messages, name="messages"),
    url(r'userTables$', views.userOnTables, name="tables"),
    url(r'allMessages$', views.allmessages, name="getMessages"),
    url(r'latestMessages/(?P<latest>\D+)$', views.allmessages, name="latestMessages"),
    url(r'newMessage$', views.newMessage, name="newMessage"),
    url(r'read/(?P<id>\d+)$', views.readThread, name="readThread"),
]