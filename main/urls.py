from django.urls import path

from main import views

urlpatterns = [
    path('home/', views.home, name="Home"),
    path('api/data/', views.get_data, name="api-data" ),
]
