from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.login_request, name="users" ),
    path('configuration_users.html', views.configuration_users, name="configuration_users" ),
    path("logout", views.logout_request, name= "logout"),
    path("change_password.html", views.change_password, name= "change_password"),

]
