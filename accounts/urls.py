from django.urls import path
from . import views


urlpatterns = [
  path('', views.dashboard, name='dashboard'),

  path('login/', views.loginPage, name='login'),
  path('logout/', views.logoutPage, name='logout'),
  path('register/', views.registerPage, name='register'),
  path('user/', views.userPage, name='user'),

  path('settings/', views.settingsPage, name='settings'),
]