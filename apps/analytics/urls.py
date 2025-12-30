"""
URLs para análisis estadísticos
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.analytics_menu, name='analytics_menu'),
    path('descriptive/', views.descriptive_stats, name='descriptive_stats'),
    path('correlation/', views.correlation_analysis, name='correlation_analysis'),
    path('distribution/', views.access_distribution, name='access_distribution'),
    path('comparison/', views.group_comparison, name='group_comparison'),
    path('trends/', views.temporal_trends, name='temporal_trends'),
    path('custom/', views.custom_panel, name='custom_panel'),
]
