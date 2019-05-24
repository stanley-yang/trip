from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.index), #login and register page
    url(r'^login$', views.login), #POST for login
    url(r'^register$', views.register), #POST for register
    url(r'^dashboard$', views.dashboard), #success/dashboard page
    url(r'^remove/(?P<id>\d+)$', views.remove), #remove trip route
    url(r'^join/(?P<id>\d+)$', views.join), #join trip route
    url(r'^cancel/(?P<id>\d+)$', views.cancel), #cancel trip route    
    url(r'^trip/(?P<id>\d+)$', views.trip), #show trip info page
    url(r'^edit/(?P<id>\d+)$', views.edit), #edit trip page
    url(r'^doedit$', views.doedit), #POST for edit
    url(r'^newtrip$', views.newtrip), #new trip page
    url(r'^donewtrip$', views.donewtrip), #POST for new trip
    url(r'^logout$', views.logout), #logout page
    url(r'^notlogged$', views.notlogged), #notlogged in

]