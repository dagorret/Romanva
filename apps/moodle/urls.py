"""
URLs para la app de Moodle
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('panel/', views.panel_view, name='panel'),
    path('never-users/', views.never_users_view, name='never_users'),
]
