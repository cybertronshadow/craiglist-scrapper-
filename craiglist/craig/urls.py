from . import views
from django.urls import path

urlpatterns = [
    path('loginpage/', views.loginpage, name='loginpage'),
    path('logoutuser/', views.logoutuser, name='logoutuser'),
    path('registeruser/', views.registeruser, name='registeruser'),
    path('', views.home, name='home'),
    path('new_search/', views.new_search, name='new_search'),

]
