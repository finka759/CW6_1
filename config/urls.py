from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('client/', include('client.urls', namespace='client')),
    path('', include('mailing.urls', namespace='mailing')),
    path('mailing/', include('mailing.urls', namespace='mailing')),
    path('message/', include('mailing.urls', namespace='message')),
]
