"""
Admin para análisis estadísticos
"""
from django.contrib import admin
from .models import SavedAnalysis


@admin.register(SavedAnalysis)
class SavedAnalysisAdmin(admin.ModelAdmin):
    list_display = ['name', 'analysis_type', 'created_at', 'updated_at']
    list_filter = ['analysis_type', 'created_at']
    search_fields = ['name', 'description']
    date_hierarchy = 'created_at'
