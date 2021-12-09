from django.urls import path

from . import views

urlpatterns = [
    path('', views.irrigation, name="irrigation"),
]
