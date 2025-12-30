"""
Modelos para análisis estadísticos
"""
from django.db import models


class SavedAnalysis(models.Model):
    """Análisis guardados por el usuario"""
    name = models.CharField(max_length=255, verbose_name='Nombre')
    description = models.TextField(blank=True, verbose_name='Descripción')
    analysis_type = models.CharField(max_length=50, verbose_name='Tipo de análisis')
    parameters = models.JSONField(verbose_name='Parámetros')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creado')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Actualizado')

    class Meta:
        verbose_name = 'Análisis guardado'
        verbose_name_plural = 'Análisis guardados'
        ordering = ['-created_at']

    def __str__(self):
        return self.name
