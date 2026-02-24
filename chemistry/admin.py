# Register of the models here.

from django.contrib import admin
from .models import MLModelMetadata, NMRTest, PredictionHistory

# This makes the models appear in the admin dashboard
# admin.site.register(MLModelMetadata)
admin.site.register(PredictionHistory)

@admin.register(MLModelMetadata)
class MLModelMetadataAdmin(admin.ModelAdmin):
    # Use only fields that actually exist in your models.py
    list_display = ('target_functionality', 'joblib_path', 'scaler_path')

@admin.register(NMRTest)
class NMRTestAdmin(admin.ModelAdmin):
    list_display = ('compound_name', 'created_at')
