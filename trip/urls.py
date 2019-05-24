from django.conf.urls import url, include

urlpatterns = [
    url(r'^', include('apps.trip_app.urls')),
]