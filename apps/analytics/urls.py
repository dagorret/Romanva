"""
URLs para análisis estadísticos
"""
from django.urls import path
from . import views

urlpatterns = [
    # Menú principal
    path('', views.analytics_menu, name='analytics_menu'),

    # Análisis básicos
    path('descriptive/', views.descriptive_stats, name='descriptive_stats'),
    path('correlation/', views.correlation_analysis, name='correlation_analysis'),
    path('distribution/', views.access_distribution, name='access_distribution'),
    path('comparison/', views.group_comparison, name='group_comparison'),
    path('trends/', views.temporal_trends, name='temporal_trends'),
    path('custom/', views.custom_panel, name='custom_panel'),

    # Análisis avanzados
    path('roles/', views.role_analysis, name='role_analysis'),
    path('regression/', views.regression_analysis, name='regression_analysis'),
    path('clustering/', views.clustering_analysis, name='clustering_analysis'),
    path('survival/', views.survival_analysis, name='survival_analysis'),
    path('heatmap/', views.heatmap_activity, name='heatmap_activity'),
    path('pca/', views.pca_analysis, name='pca_analysis'),

    # Estadísticas avanzadas (Big Data & IA)
    path('churn/', views.churn_prediction, name='churn_prediction'),
    path('engagement/', views.engagement_patterns, name='engagement_patterns'),
    path('network/', views.course_network, name='course_network'),
    path('predictive/', views.predictive_trends, name='predictive_trends'),
    path('segmentation/', views.smart_segmentation, name='smart_segmentation'),
    path('anomalies/', views.anomaly_detection, name='anomaly_detection'),
]
